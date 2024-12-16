import utils.auxiliary


log = utils.auxiliary.Auxiliary(__name__)
log.set_config()


class File():  # Making a class to handle files
    def __init__(self, path):
        self.path = path

    def open_file(self):
        if utils.auxiliary.verbose:
            log.logger.info(f"{utils.auxiliary.BLUE}[*]{utils.auxiliary.RESET}"
                            f"Opening file {self.path}")
        self.file = open(self.path, "r")
        return self.file

    def __del__(self):
        if utils.auxiliary.verbose:
            log.logger.info(f"{utils.auxiliary.BLUE}[*]{utils.auxiliary.RESET}"
                            f"Closing file {self.path}")
        self.file.close()
