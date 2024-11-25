import requests
import re

from bs4 import BeautifulSoup

def crawl_webpage_endpoints(url):
    endpoints_list = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        # Getting our links
        match = re.search('\/(.+)\?(.+)\=(.+)', href)
        if match:
            # Initializing list with first link
            if len(endpoints_list) == 0:
                endpoints_list.append(href)
                print(f"\n[*] Crawler: adding first endpoint {href}")
            # Appending links with unique first group
            if match.group(1) not in endpoints_list[-1]:
                endpoints_list.append(href)
                print(f"[*] Crawler: adding unique endpoint {href}")
    return endpoints_list