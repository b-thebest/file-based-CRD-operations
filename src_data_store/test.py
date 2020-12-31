'__author__: b-thebest (Burhanuddin Kamlapurwala)'

from testing.test_operations import test_read, test_create, test_delete
from os import path
from configurations.db_config import DATA_PATH, DATA_FILE_NAME
from time import sleep

file_path = path.join(DATA_PATH, DATA_FILE_NAME)

#Insert demo data in database
test_create().start()

#Insert data with threading
#test_create(threaded=True).start()

#Reading data from database
test_read().start()

#Deleting demo data from database
test_delete().start()

print("\nTrying to read data after time to live")
sleep(3)
test_read().start(custom_key="leaf")

