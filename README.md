author: b-thebest

# file-based-CRD-operations
This repository is created against assignment given by Freshworks

As given in the problem statement, we have to implement CRD operations on JSON file.
For using these operations (Create, Read, Delete) one can do it using three ways:
1. Using REST APIs
2. By using operation functions in different module for mentioned data
3. By importing data from another JSON file

To understand in detail How to use this project, you can through docs available in repository.

Result samples can be found at location https://github.com/b-thebest/file-based-CRD-operations/tree/main/result_samples 


# Environment Setup
  1.Operating system : Ubuntu 18.04
  
  2.Python >= 3.6
  
  3.Install Python requirements using following command
  
      python3 -m pip install -r requirements.txt
  4.Run the project
  
      a. run python3 flask_app.py Default database will be selected for operations
      b. run python3 flask_app.py --path "path/to/your/file/or/database"


# Configurations
To give more flexibility, some configurations added which can be modified as per the requirements. 

There are two configuration files can be found [here](https://github.com/b-thebest/file-based-CRD-operations/tree/main/src_data_store/configurations)

**api_settings.py** contains informations about host, port and debugging
**db_config.py** contains setttings related to database.

#### NOTE: If you set *OVERWRITE_TTL* to *True* in [db_config.py](https://github.com/b-thebest/file-based-CRD-operations/blob/main/src_data_store/configurations/db_config.py) then it will start overwriting expired items too.


# Test Setup
*test.py* file is created under src_data_store to run basic test cases on test_db.json

To run basic test cases, run following command:
```python3 test.py```

NOTE by default this file runs on basic test cases created in following files which can be modified by user
1. [create_test_cases.json](https://github.com/b-thebest/file-based-CRD-operations/tree/main/src_data_store/testing/create_test_cases.json)
2. [read_test_cases.json](https://github.com/b-thebest/file-based-CRD-operations/tree/main/src_data_store/testing/read_test_cases.json)
3. [delete_test_cases.json](https://github.com/b-thebest/file-based-CRD-operations/tree/main/src_data_store/testing/delete_test_cases.json)

To run custom test cases following ways are available:
1. pass data in dictionary format to function for example
```
from testing.test_operations import test_read, test_create, test_delete
data = {
  "someKey": {
    "attr1": "Some Name",
    "attr2": "Some Other Name"
  }
}
test_create().start(custom_data=data)
test_read().start(custom_key="someKey")
test_delete().start(custom_key="someKey")
```
2. Use JSON file to do your task simply
NOTE: file should be in JSON format. reference can be taken from [test files](https://github.com/b-thebest/file-based-CRD-operations/tree/main/src_data_store/testing)
*example*
```
from testing.test_operations import test_read, test_create, test_delete

test_create().start(custom_file="path/to/your/testcases/file")
test_read().start(custom_file="path/to/your/testcases/file")
test_delete().start(custom_file="path/to/your/testcases/file")
```


# Accessing data store as a module
This feature allows to import datastore into your file and use operations as you need. **main.py** contains the sample operations for reference
```
from src_data_store.operations.operation_functions import CRD

file_path = 'src_data_store/data/'

data = {"demo": {"name": "John", "city": "Seattle"}}

#create operation
print(CRD(file_path).create(data))
print(CRD(file_path).create({"demo2": {"name": "Bob", "city": "Agra", "Time-To-Live": 120}}))
print(CRD(file_path).create({"demo3": {"name": "Alan", "city": "Indore", "Time-To-Live": 60}}))

#read operation
print(CRD(file_path).read("demo"))
print(CRD(file_path).read("demo2"))
print(CRD(file_path).read("demo3"))

#delete operation
print(CRD(file_path).delete("demo2"))
```

# REST API examples
**Create**
  url/endpoint -- http://localhost:7000/datastore/create
  
  body (type:JSON) -- 
  {
    "someKey": {
      "attr1": "Some Name",
      "attr2": "Some Other Name"
    }
  }
  
  Response:
    {
    "message": "Data inserted successfully",
    "status": "success"
  }
  
  Constraints:
  1. Value should be in JSON
  2. key length <= 32 
  3. Value size <= 16KB
  4. No spaces and special characters in key
  
**Read**
  url/endpoint -- http://localhost:7000/datastore/read
  
  params
    
    key: It should not contain special characters and spaces and should not exceed 32 characters
    
**Delete**
  url/endpoint -- http://localhost:7000/datastore/delete
  
  params
  
    key: It should not contain special characters and spaces and should not exceed 32 characters
