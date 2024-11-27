from SQLi.confirm_sqli import *
from SQLi.boolean_sqli import *
from utils.parser import *


def main():
    args = parse_args()
   #  if args.url.endswith("/")
    options = try_url_param_sqli(args.url)
    if options[2] == "True":
        try_boolean_sqli(args.url, options)


if __name__ == "__main__":
    main()
