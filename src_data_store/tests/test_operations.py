import flask
from flask import request, jsonify
from argparse import ArgumentParser
from configurations.api_settings import DEBUG, HOST, PORT
from configurations.db_config import DATA_PATH, DATA_FILE_NAME
from utils.directory import directory as director
from operations.operation_functions import CRD

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
