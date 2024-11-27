import sys

from SQLi.confirm_sqli import *
from SQLi.boolean_sqli import *
from utils.parser import *

def main():
   n = parse_args()
   options = try_url_param_sqli(n.url)
   if options[2] == "True":
      try_boolean_sqli(n.url, options)

if __name__ == "__main__":
   main()