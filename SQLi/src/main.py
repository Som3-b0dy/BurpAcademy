from SQLi.confirm_sqli import *
from SQLi.boolean_sqli import *
from SQLi.login_sqli import *
from utils.auxiliary import *
from utils.parser import *


def main():
    args = parse_args()
    options = try_url_param_sqli(args.url)
    if options[2] == "True":
        try_boolean_sqli(args.url, options)
    try_login_sqli(args.url)


if __name__ == "__main__":
    main()
