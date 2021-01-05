'__author__: b-thebest (Burhanuddin Kamlapurwala)'

from flask import request, jsonify
from argparse import ArgumentParser
from configurations.api_settings import DEBUG, HOST, PORT
from configurations.db_config import DATA_PATH, DATA_FILE_NAME
from utils.directory import directory as director
from operations.operation_functions import CRD

# Adding command line arguments to check file path
parser = ArgumentParser()
parser.add_argument('--path', help='Enter the absolute path of file', default=DATA_PATH)
parser.add_argument('--threaded', help='True will be running this process in threaded mode, default set to False', default=False)
args = parser.parse_args()

file_path = args.path
is_thread = args.threaded

#Directory creation in case of not exist
successful_creation = director(file_path).create_folder()
if not successful_creation:
    print("Permission Denied: You can not create file at location ", file_path)
    exit(0)

app = flask.Flask(__name__)
app.config["DEBUG"] = DEBUG

@app.route('/datastore/create', methods=['POST'])
def create_route():
    try:
        request_data = request.get_json(force=True)
    except Exception:
        return jsonify(
            {"status": "error", "message": "Incorrect request format: Only JSON allowed"}), 400

    ##Creating new entry for the request data
    valid, response_message = CRD(file_path, threaded=is_thread).create(request_data)
    if not valid:
        return jsonify({"status": "error", "message": response_message}), 400

    return jsonify({"status": "success", "message": response_message}), 200

@app.route('/datastore/read', methods=['GET'])
def read_route():
    key = request.args.get('key')
    if key is None:
        return jsonify({"status": "error", "message": "key is mandatory"}), 400

    #Reading data from file for a key
    found, response_message = CRD(file_path).read(key)
    if not found:
        return jsonify({"status": "error", "message": response_message}), 404

    return jsonify(response_message), 200

@app.route('/datastore/delete', methods=['DELETE'])
def delete_route():
    key = request.args.get('key')

    if key is None:
        return jsonify({"status": "error", "message": "key is mandatory"}), 400

    #Deleting data associated with key
    found, response_message = CRD(file_path).delete(key)
    if not found:
        return jsonify({"status": "error", "message": response_message}), 404

    return jsonify({"status": "success", "message": response_message}), 200

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, threaded=True)