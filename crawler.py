import os

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": f"PersonalProjectCrawler/1.0 (contact: {os.environ.get('CRAWLER_CONTACT_EMAIL', 'unknown')})"
}

tags_to_extract = ['h1', 'h2', 'h3', 'p']

def extract_text_links(soup):
    found_links_text = soup.find_all('a')
    all_found_links = [link.get('href') for link in found_links_text if link.get('href')]
    return all_found_links

def extract_text_tags(soup):
    page_dict = {}
    for tag in tags_to_extract:
        found_tags = soup.find_all(tag)
        text_in_tags = [tag.get_text().strip() for tag in found_tags]
        page_dict[tag] = text_in_tags
    return page_dict


def bfs(initial_page):
    counter = 1
    visited = set()
    to_visit = [initial_page]
    while to_visit:
        current = to_visit.pop()
        if current in visited:
            continue
        visited.add(current)
        resp = requests.get(current, headers=headers, timeout=10)
        if resp.status_code not in range(200, 300):
            continue
        print(str(counter) + ' Preprocessing page ' + str(current))
        soup = BeautifulSoup(resp.text, 'html.parser')
        page_dict = extract_text_tags(soup)
        page_dict['links'] = extract_text_links(soup)

        print(page_dict)
        # to_visit.extend(page_dict['links'])
        counter += 1

def main():
    bfs('https://en.wikipedia.org/wiki/Absolute_pitch')

if __name__ == '__main__':
    main()