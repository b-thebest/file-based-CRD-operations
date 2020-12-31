'__author__: b-thebest (Burhanuddin Kamlapurwala)'

from os import path
from json import dump
class cleaner:
    def __init__(self, file_path):
        self.file_path = file_path

    def clean(self):
        if path.isfile(self.file_path):
            if self.file_path.endswith(".json"):
                dump({}, open(self.file_path, 'w+'), indent=3)
            else:
                open(self.file_path, 'w+')
            print("file cleaned successfully")
        else:
            print("No file exist for the given path")