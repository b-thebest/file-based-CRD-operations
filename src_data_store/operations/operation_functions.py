import json
import fcntl
import threading
from os import path
from datetime import datetime, timedelta
from dateutil.parser import parse
from configurations.db_config import DATA_FILE_NAME, OVERWRITE_TTL
from sys import getsizeof
import fcntl
from time import time

class CRD:
    def __init__(self, file_path, threaded=False):
        self.file_path = file_path
        self.lock = threading.Lock()
        self.threaded = threaded

    def check_data_validity(self, data, onlyKey=False):
        if onlyKey:
            # check type of key
            if not isinstance(data, str) or not data.isalnum():
                return (False, "TypeError: Key should be of type string for '" + str(data) + "'")
            # check length of key
            if len(data) > 32:
                return (False, "Invalid key length: Key can not be larger than 32 characters for " + str(data))
        else:
            for key, value in data.items():
                # check type of key
                if not isinstance(key, str) or not key.isalnum():
                    return (False, "TypeError: Key should be of type string for '" + str(key) + "'")
                # check length of key
                if len(key) > 32:
                    return (False, "Invalid key length: Key can not be larger than 32 characters for " + str(key))
                # Check type of value
                if not isinstance(value, dict):
                    return (False, "TypeError: Data value should be json for key " + str(key))

                # Check data value size is under 16KB
                value_data = json.dumps(value)
                if getsizeof(value_data) > 16384:
                    return (False, "Data limit of value is 16KB exceeded for " + str(key))

    def check_ttl(self, dead):
        if dead < int(time()):
            return False
        return True

    def create(self, req_data):
        if not isinstance(req_data, dict):
            return (False, "Incorrect request format. JSON expected")

        data = json.dumps(req_data)
        if getsizeof(data) > 2**30:
            return (False, "Data size limit exceed 1GB")

        error = self.check_data_validity(req_data)
        if error:
            return error

        if path.isfile(self.file_path):
            store = self.file_path
        else:
            store = self.file_path + DATA_FILE_NAME

        data_store = open(store)
        #Locking system
        fcntl.flock(data_store, fcntl.LOCK_EX)
        file_data = json.load(data_store)
        fcntl.flock(data_store, fcntl.LOCK_UN)

        file_data_dict = json.dumps(file_data)
        if getsizeof(file_data_dict) >= 2 **30:
            return (False, "Memory full. File size limit exceeded")

        for key in file_data.keys():
            if key in req_data.keys():
                target = file_data[key]
                if not(OVERWRITE_TTL and ("Time-To-Live" in target.keys()) and not self.check_ttl(target["dead_time"])):
                    return (False, "KeyError: '" + str(key) +  "' Key already exist")

        data_to_write = {}
        if self.threaded:
            def thread_write(json_keys):
                for key in json_keys:
                    row = req_data[key]
                    if "Time-To-Live" in row.keys():
                        row["dead_time"] = row["Time-To-Live"] + int(time())
                    data_to_write[key] = row

            n_threads = 4 #Number of threads permissible
            json_keys = req_data.keys()
            batch_size = len(json_keys) // n_threads
            active_threads = []
            for i in n_threads:
                firstIndex = i * batch_size
                lastIndex = (i+1) * batch_size if (i+1) < n_threads else None
                active_threads.append(threading.Thread(target=thread_write, args=(json_keys[firstIndex:lastIndex],), name = "thread" + str(i)))
                active_threads[-1].start()

            for task in active_threads:
                task.join()

        else:
            json_keys = req_data.keys()
            for key in json_keys:
                row = req_data[key]
                if "Time-To-Live" in row.keys():
                    row["dead_time"] = row["Time-To-Live"] + int(time())
                data_to_write[key] = row

        file_data.update(data_to_write)
        data_store = open(store, 'w+')
        fcntl.flock(data_store, fcntl.LOCK_EX)
        json.dump(file_data, data_store, indent=3)
        fcntl.flock(data_store, fcntl.LOCK_UN)

        return (True, "Data inserted successfully")

    def read(self, key):
        error = self.check_data_validity(key, onlyKey=True)
        if error:
            return error

        if path.isfile(self.file_path):
            store = self.file_path
        else:
            store = self.file_path + DATA_FILE_NAME

        data_store = open(store)
        # Locking system
        fcntl.flock(data_store, fcntl.LOCK_EX)
        file_data = json.load(data_store)
        fcntl.flock(data_store, fcntl.LOCK_UN)

        if key not in file_data.keys():
            return (False, "KeyError: No data for given key")

        target = file_data[key]
        if "dead_time" in target.keys():
            if not self.check_ttl(target["dead_time"]):
                return (False, "Data expired")
            else:
                #Deleting irrelevant data
                del target["dead_time"]

        return (True, target)

    def delete(self, key):
        error = self.check_data_validity(key, onlyKey=True)
        if error:
            return error

        if path.isfile(self.file_path):
            store = self.file_path
        else:
            store = self.file_path + DATA_FILE_NAME

        data_store = open(store)
        # Locking system
        fcntl.flock(data_store, fcntl.LOCK_EX)
        file_data = json.load(data_store)
        fcntl.flock(data_store, fcntl.LOCK_UN)

        if key not in file_data.keys():
            return (False, "KeyError: No data for given key")

        target = file_data[key]
        if not self.check_ttl(target["dead_time"]):
            return (False, "Data expired")

        ##Deleting data from key
        del file_data[key]

        data_store = open(store, 'w+')
        fcntl.flock(data_store, fcntl.LOCK_EX)
        json.dump(file_data, data_store)
        fcntl.flock(data_store, fcntl.LOCK_UN)

        return (True, "Data value deleted successfully")