from __future__ import print_function
import sys
import json
import argparse

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

eprint = sys.stderr.write

url = r'''http://fanyi.youdao.com/openapi.do'''

data = {
    'keyfrom': 'hidict',
    'key': '1217482697',
    'type': 'data',
    'doctype': 'json',
    'version': '1.1',
}

def get_response(word):
    data['q'] = word
    url_values = urlencode(data)
    full_url = url + '?' + url_values
    try:
        result = urlopen(full_url).read()
    except:
        eprint("ERROR: Can not make network connection")
        return None
    else:
        try:
            return json.loads(result, encoding='utf-8')
        except:
            eprint("ERROR: Can not translate %s" % word)
            return None

def is_valid_result(result):
    error_code = result.get('errorCode')
    if error_code == 0:
        return True
    else:
        eprint("ERROR: can't translate %s" % result.get("query"))
        return False

def show_generalization(result):
    translation = result.get('translation')
    if translation:
        print('Translation:')
        for t in translation:
            print('\t', t.encode('utf-8').decode('utf-8'))


def show_explains(result):
    basic = result.get('basic')
    if basic:
        explains = basic.get('explains')
        if explains:
            print('Explains:')
            for e in explains:
                print('\t', e.encode('utf-8').decode('utf-8'))

def show_web(result):
    web = result.get('web')
    if web:
        for item in web:
            print("Key: ", item.get('key').encode('utf-8'))
            for v in item.get('value'):
                print('\tvalue: ', v.encode('utf-8').decode('utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("word", type=str,
                        help="the word that you want to translate")
    parser.add_argument("-g", "--summary", help="show summary translation",
                        action="store_true")
    parser.add_argument("-b", "--base", help="show base explains",
                        action="store_true")
    parser.add_argument("-w", "--web", help="show web translation",
                        action="store_true")
    args = parser.parse_args()
    
    esc = r''',./<>?:;'"{}[]|\~`!@#$%^&*()-_=+'''
    
    word = args.word.strip(esc)
    print('[', word, end=' ] ')
    
    
    result = get_response(word)
    
    if args.summary:
        show_generalization(result)
    if args.base:
        show_explains(result)
    if args.web:
        show_web(result)

if __name__ == '__main__':
    main()
    
