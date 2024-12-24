import utils.auxiliary


log = utils.auxiliary.Auxiliary(__name__)
log.set_config()


class File():  # Making a class to handle files
    def __init__(self, path: str):
        self.path = path
        self.open_file()

    def open_file(self):
        if utils.auxiliary.verbose:
            log.logger.info(f"{utils.auxiliary.BLUE}[*] "
                            f"{utils.auxiliary.RESET}"
                            f"Opening file {self.path}")
        self.file = open("./utils/files/" + self.path, "r")
        return self.file

    def __del__(self):
        if utils.auxiliary.verbose:
            log.logger.info(f"{utils.auxiliary.BLUE}[*] "
                            f"{utils.auxiliary.RESET}"
                            f"Closing file {self.path}")
        self.file.close()
