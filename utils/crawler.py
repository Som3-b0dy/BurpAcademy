import re

import requests
from bs4 import BeautifulSoup


def collect_unique_endpoints(match, href, endpoints: list):
    # Initializing list with first link
    if len(endpoints) == 0:
        endpoints.append(href)
        print(f"\n[*] Crawler: adding first endpoint {href}")
    # Appending links with unique first group
    counter = 0
    for endp in endpoints:
        if match.group(1) not in endp:
            counter += 1
    if len(endpoints) == counter:
        endpoints.append(href)
        print(f"[*] Crawler: adding unique endpoint {href}")


def crawl_webpage_endpoints(url) -> list:
    endpoints = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        # Looking for links with regex
        match = re.search('\/(.+)\?(.+)\=(.+)', href)
        if match:
            collect_unique_endpoints(match, href, endpoints)
    return endpoints
