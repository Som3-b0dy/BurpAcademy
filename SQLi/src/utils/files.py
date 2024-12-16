from utils.auxiliary import *


class File():
    def __init__(self, path):
        self.path = path

    def open_file(self):
        self.file = open(self.path, "r")
        return self.file

    def __del__(self):
        self.file.close()
