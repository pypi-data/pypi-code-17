# -*- coding: utf-8 -*-
# this module provide function for work with http://eais.rkn.gov.ru/
# You need API key from anti-captcha.com for this module

import os
import time
import argparse

import requests
from pyquery import PyQuery as pq
from antigate import AntiGate


def query(domain, api_key, verbose):
    """Get information about domain/ip from RKN reestr"""

    def solve_captcha(cap_url, antigate_api_key, s, verbose=False):
        """Solve captcha woth antigate
        Get Api key from anti-captcha.com"""
        gate = AntiGate(antigate_api_key, auto_run=False)
        cap = s.get(cap_url)
        try:
            os.stat('tmp/')
        except IOError:
            os.mkdir('tmp/')
        with open("tmp/cap.jpg", "wb+") as f:
            f.write(cap.content)
        captcha_id1 = gate.send('tmp/cap.jpg')
        if verbose:
            print ("Solving captcha, please wait...")
        time.sleep(10)
        captcha = gate.get(captcha_id1)
        if verbose:
            print ("Captcha decoded: %s" % captcha)
        return captcha

    if verbose:
        print("Loading http://eais.rkn.gov.ru/")
    s = requests.Session()
    s.headers.update({'user-agent':
                      ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) '
                       'Gecko/20100101 Firefox/53.0')})
    
    r = s.get('http://eais.rkn.gov.ru/')
    parse = pq(r.text)
    parse.make_links_absolute(base_url="http://eais.rkn.gov.ru/")
    captcha_url = parse('img#captcha_image').attr('src')
    if verbose:
        print ("Captcha url: %s" % captcha_url)
    captcha = solve_captcha(captcha_url, api_key, s, verbose)
    data = {"act": ('', "search"),
            "secretcodeId": ('', ''),
            "searchstring": ('', domain),
            "secretcodestatus": ('', captcha)}

    # I use files for data
    # because eais.rkn use multipart form
    r = s.post('http://eais.rkn.gov.ru/', files=data)

    parse = pq(r.text)
    message = parse('div.messageFlash:first').html()
    message_text = parse('div.messageFlash:first').text()
    if "TblGrid" in message:
        if "ограничивается к сайту" in message:
            result = "Сайт в реестре, доступ ограничивается"
        elif "доступ не ограничивается" in message:
            result = "Сайт в реестре, доступ не ограничивается"
    else:
        result = message_text
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('domain', help='Domain to check, example: site.ru')
    parser.add_argument('api_key', help='Antigate API key for captcha recognition')
    parser.add_argument('--verbose', action="store_true",
                        help='Display some debug information')

    args = parser.parse_args()
    print (query(args.domain, args.api_key, args.verbose))
