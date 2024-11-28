import re

import requests
from bs4 import BeautifulSoup

from utils.auxiliary import *


def collect_unique_endpoints(match, href, endpoints: list):
    l = Auxiliary(__name__)
    l.set_config()
    if len(endpoints) == 0:  # Initializing list with first link
        endpoints.append(href)
        l.logger.info(f"[*] Adding first endpoint {href}")
    counter = 0
    for endp in endpoints:  # Appending links with unique first group
        if match.group(1) not in endp:
            counter += 1
    if len(endpoints) == counter:
        endpoints.append(href)
        l.logger.info(f"[*] Adding unique endpoint {href}")


def crawl_webpage_endpoints(url) -> list:
    endpoints = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        # Looking for links with regex
        match = re.search('^\/(.+)\?(.+)\=(.+)', href)
        if match:
            collect_unique_endpoints(match, href, endpoints)
    return endpoints
