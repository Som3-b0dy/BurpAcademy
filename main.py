import logging

from SQLi.confirm_sqli import *
from SQLi.boolean_sqli import *
from utils.auxiliary import *
from utils.parser import *


def main():
    l = Auxiliary(moduleName=__name__)
    l.set_config()
    l.logger.info('Log from main')
    args = parse_args()
    options = try_url_param_sqli(args.url)
    if options[2] == "True":
        try_boolean_sqli(args.url, options)


if __name__ == "__main__":
    main()
