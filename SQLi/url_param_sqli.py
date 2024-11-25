import requests

from utils.crawler import *

def try_url_param_sqli(url):
    endpoints_list = crawl_webpage_endpoints(url)
    for endp in endpoints_list:
        r = requests.get(url = url + endp + "'")
        if r.status_code == 500:
            print(f"[*] Possible SQLi is found on endpoint {endp}'")
            r = requests.get(url = url + endp + "'--")
            if r.status_code == 200:
                print(f"[+] Confirmed SQLi is found on endpoint {endp}'--")
        else:
            print(f"[-] Endpoint {endp} is likely not vulnerable to SQLi")