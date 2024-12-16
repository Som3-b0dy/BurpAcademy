import logging

'''
    options[0] -> endpoints to try SQLi against
    options[1] -> type of comment used in database
    options[2] -> number of columns to try union SQLi
    options[3] -> column indexes that accept string
'''

options = [[], "", "", []]

RED = "\x1b[31;1m"
GREEN = "\x1b[32;1m"
YELLOW = "\x1b[33;1m"
BLUE = "\x1b[34;1m"
RESET = "\x1b[0m"


class Auxiliary:  # Defining a logger template to use
    def __init__(self, moduleName=None):
        default_name = __name__
        if moduleName:
            self.logger = logging.getLogger(moduleName)
        else:
            self.logger = logging.getLogger(default_name)

    @staticmethod
    def set_config():  # Making a more comfortable logger
        logging.basicConfig(
            format='\x1b[33;1m{asctime}\x1b[0m'
            ':{levelname}:'
            '\x1b[31;1m[{name}]\x1b[0m'
            '\x1b[30;1m[{threadName}]\x1b[0m'
            '\n{message}',
            datefmt='%H:%M:%S',
            level=logging.INFO,
            style='{'
        )
