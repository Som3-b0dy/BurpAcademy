import sys

from SQLi.confirm_sqli import *

def main():
   try:
      url = sys.argv[1]
      try_url_param_sqli(url)
   except IndexError:
      print("[!] url param is required")
      print(f"[!] python3 {sys.argv[0]} <url>")

if __name__ == "__main__":
   main()