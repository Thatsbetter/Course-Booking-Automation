import json
import os


class Credential():
    def __init__(self):
        dir_name = os.path.dirname(__file__)
        file_path = os.path.join(dir_name, 'credential.json')
        with open(file_path, 'r') as myfile:
            data = myfile.read()
        self.obj = json.loads(data)
    def get_username(self):
        return self.obj["username"]

    def get_password(self):
        return self.obj["password"]
