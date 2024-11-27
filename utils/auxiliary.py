import logging


class Auxiliary:  # Defining a logger template to use
    def __init__(self, moduleName=None):
        if moduleName:
            self.logger = logging.getLogger(moduleName)
        else:
            self.logger = logging.getLogger(__name__)

    def set_config(self):  # Making a more comfortable logger
        logging.basicConfig(
            format='{asctime}:{levelname}:[{name}][{threadName}]\n{message}',
            datefmt='%H:%M:%S',
            level=logging.INFO,
            style='{'
        )
