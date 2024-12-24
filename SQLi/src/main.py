from SQLi.confirm_sqli import *
from SQLi.login_sqli import *
from utils.parser import *


def main():
    args = parse_args()
    try_url_param_sqli(args.url)
    # try_login_sqli(args.url)


if __name__ == "__main__":
    main()
