import sys

from SQLi.confirm_sqli import *
from SQLi.boolean_sqli import *

def main():
   try:
      url = sys.argv[1]
      options = try_url_param_sqli(url)
      if options[2] == "True":
         try_boolean_sqli(url, options)
   except IndexError:
      print("[!] url param is required")
      print(f"[!] python3 {sys.argv[0]} <url>")

if __name__ == "__main__":
   main()