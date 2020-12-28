import flask
import json
from flask import request, jsonify
from os import path
from argparse import ArgumentParser
from src_data_store.configurations.api_settings import DEBUG, HOST, PORT
from src_data_store.configurations.db_config import DATA_PATH, DATA_FILE_NAME
from src_data_store.utils.directory import directory as director
from src_data_store.operations.operation_functions import CRD

# Adding command line arguments to check file path
parser = ArgumentParser()
parser.add_argument('--path', help='Enter the absolute path of file', default=DATA_PATH)
args = parser.parse_args()

file_path = args.path

#Directory creation in case of not exist
successful_creation = director(file_path).create_folder()
if not successful_creation:
    print("Permission Denied: You can not create file at location ", file_path)
    exit(0)

class test_create:
    def __init__(self, file_path, threaded):
        self.file_path = file_path
        self.threaded = threaded

    def start_test(self, data, threaded=False):
        if not isinstance(data, dict):
            print("Incorrect data format: Only JSON allowed")
            return False

        ##Creating new entry for the request data
        valid, response_message = CRD(self.file_path, threaded=threaded).create(data)
        if not valid:
            print(response_message)
            return False

        print(response_message)
        return True

    def start(self, custom_data=None, custom_file=None, threaded=False):
        if custom_data:
            return self.start_test(custom_data, threaded)

        elif custom_file:
            if not path.isfile(custom_file):
                print(custom_file + " not found")
                return False
            data_file = json.dumps(open(custom_file))
            return self.start_test(data_file, threaded)

        else:
            data_file = json.dumps(open('create_test_cases.json'))
            return self.start_test(data_file, threaded)

class test_read:
    def __init__(self, file_path):
        self.file_path = file_path

    def start_test(self, key):
        # Reading data from file for a key
        found, response_message = CRD(file_path).read(key)
        if not found:
            print(response_message)
            return False

        print(response_message)
        return True

    def start(self, custom_key=None, custom_file=None):
        if custom_key:
            print("Key : ", custom_key, "Response : ", end='')
            self.start_test(custom_key)

        elif custom_file:
            if not path.isfile(custom_file):
                print(custom_file + " not found")
                return False
            file_data = json.dumps(open(custom_file))
            for key in file_data['keys']:
                print("Key : ", key, "Response : ", end='')
                self.start_test(key)

        else:
            file_data = json.dumps(open("read_test_cases.json"))
            for key in file_data['keys']:
                print("Key : ", key, "Response : ", end='')
                self.start_test(key)

class test_delete:
    def __init__(self, file_path):
        self.file_path = file_path

    def start_test(self, key):
        # Deleting data from file for a key
        found, response_message = CRD(file_path).delete(key)
        if not found:
            print(response_message)
            return False

        print(response_message)
        return True

    def start(self, custom_key=None, custom_file=None):
        if custom_key:
            print("Key : ", custom_key, "Response : ", end='')
            self.start_test(custom_key)

        elif custom_file:
            if not path.isfile(custom_file):
                print(custom_file + " not found")
                return False
            file_data = json.dumps(open(custom_file))
            for key in file_data['keys']:
                print("Key : ", key, "Response : ", end='')
                self.start_test(key)

        else:
            file_data = json.dumps(open("delete_test_cases.json"))
            for key in file_data['keys']:
                print("Key : ", key, "Response : ", end='')
                self.start_test(key)