from testing.test_operations import test_read, test_create, test_delete
from os import path
from configurations.db_config import DATA_PATH, DATA_FILE_NAME

file_path = path.join(DATA_PATH, DATA_FILE_NAME)

#Insert demo data in database
test_create(file_path).start()
#Insert data with threading
test_create(file_path, threaded=True).start()

#Reading data from database
test_read(file_path).start()

#Deleting demo data from database
test_delete(file_path).start()
