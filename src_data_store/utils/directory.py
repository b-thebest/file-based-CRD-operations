from os import path, makedirs, stat

class directory:
    def __init__(self, file_path):
        self.file_path = file_path

    def create_folder(self):
        try:
            makedirs(self.file_path, mode=0o777, exist_ok=True)
        except PermissionError:
            return False
        return True

    def check_file_size(self):
        if stat(self.file_path).st_size >= 2**30:
            return False
        return True
