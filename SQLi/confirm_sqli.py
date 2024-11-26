import requests

from utils.crawler import *

def try_url_param_sqli(url) -> list:
    options = [[], "", "False"]
    endpoints = crawl_webpage_endpoints(url)
    for endp in endpoints:
        r = requests.get(url = url + endp + "'")
        if r.status_code == 500:
            print(f"[*] Possible SQLi is found on endpoint {endp}'")
            r_1 = requests.get(url = url + endp + "'--")
            if r_1.status_code == 200:
                print(f"[+] Confirmed SQLi is found on endpoint {endp}'--")
                options[0].append(endp)
                options[1] = "--"
                options[2] = "True"
            r_2 = requests.get(url = url + endp + "'%23")
            if r_2.status_code == 200:
                print(f"[+] Confirmed SQLi is found on endpoint {endp}'#")
                options[0].append(endp)
                options[1] = "#"
                options[2] = "True"
        else:
            print(f"[-] Endpoint {endp} is likely not vulnerable to SQLi")
    return options 