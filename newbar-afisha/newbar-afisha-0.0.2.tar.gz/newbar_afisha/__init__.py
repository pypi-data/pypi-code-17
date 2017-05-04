#!/usr/bin/env python

import bs4
import requests

url = 'https://vk.com/newbarekb'


def afisha_link():
    main_page = requests.get(url).content
    soup = bs4.BeautifulSoup(main_page, 'html.parser')
    for link in soup.find_all('a'):
        if link.get('class') == [u'wide_link']:
            return 'https://vk.com' + link.get('href')
    raise ValueError


def parse_events(afisha_url):
    afisha = requests.get(afisha_url).content
    soup = bs4.BeautifulSoup(afisha, 'html.parser')
    for tr in soup.table.find_all('tr'):
        yield " ".join([th.text.strip().replace('\n', '') for th in tr.find_all('th')]).strip()


def main():
    for event in parse_events(afisha_link()):
        print event


if __name__ == '__main__':
    main()

