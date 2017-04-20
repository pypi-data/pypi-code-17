#!/usr/bin/env python
from __future__ import division

from sys import argv, exit, stderr, stdout
from os.path import expanduser
from os import unlink
import requests
import requests.exceptions
import json
from urllib import unquote
import argparse
from datetime import datetime, timedelta
from time import sleep
import re


__all__ = ['VERSION_NUMBER', 'VERSION_DATE', 'SECONDS_TO_WAIT', 'get_url_info', 'get_token', 'get_download_url_data',
           'create_download_link', 'download_url']

VERSION_NUMBER = "2.3.1"
VERSION_DATE = "April 2017"
SECONDS_TO_WAIT = 30

def get_url_info(url):
    # parse url

    origin = re.search('^((http[s]?):\/)?\/?([\w.-]+)',url).group(0)
    origin = origin.lower()

    url_info = {
        'orig_url': url,
        'origin': origin,
        'host':origin.replace('http://','').replace('https://', '')
    }

    # try to urldecode
    try:
        url = unquote(url)
    except:
        pass
    url = url.lower()

    parts = url.split('/')

    try:
        for i in xrange(len(parts)):
            if parts[i] == 'watch':
                i += 1
                url_info['name'] = parts[i]

            if parts[i] == 'season':
                i += 1
                url_info['season'] = parts[i]

            if parts[i] == 'episode':
                i += 1
                url_info['episode'] = parts[i]

        url_info['sid_id'] = url_info['name'].split('-', 1)[0]
        url_info['name'] = url_info['name'].split('-', 1)[1]

        url_info['filename'] = '{name}_s{season}_e{episode}.mp4'.format(
            name=url_info['name'],
            season=url_info['season'].zfill(2),
            episode=url_info['episode'].zfill(2)
        )
    except Exception, ex:
        print ex
        raise Exception('Missing url elements.\nSample url: {}'.format(
            'http://www.sdarot.pm/watch/82-%D7%9E%D7%A9%D7%97%D7%A7%D7%99-%D7%94%D7%9B%D7%A1-game-of-thrones/season/4/episode/6'))

    return url_info

def get_token(url_info):
    form = {
        'preWatch': True,
        'SID': url_info['sid_id'],
        'season': url_info['season'],
        'ep': url_info['episode']
    }

    headers = {
        'DNT': '1',  # Do not track request (optional)
        'Referer': url_info['orig_url'],
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",  # be IE 11.0
        'Host': url_info['host'],
        'Origin': url_info['origin'],
        'Accept-Language': "he-IL,he;q=0.8,en-US;q=0.6,en;q=0.4",
    }

    r = requests.post('{}/ajax/watch'.format(url_info['origin']), data=form, headers=headers)

    if r.status_code == 200:
        # save response cookies (needed to procceed download)
        url_info['cookies'] = r.cookies
        return r.text
    else:
        return False

def get_download_url_data(url_info):
    form = {
        'watch': True,
        'token': url_info['token'],
        'serie': url_info['sid_id'],
        'season': url_info['season'],
        'episode': url_info['episode']
    }

    headers = {
        'DNT': '1',  # Do not track request (optional)
        'Referer': url_info['orig_url'],
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",  # be IE 11.0
        'Host': url_info['host'],
        'Origin': url_info['origin'],
        'Accept-Language': "he-IL,he;q=0.8,en-US;q=0.6,en;q=0.4",
    }

    r = requests.post('{}/ajax/watch'.format(url_info['origin']), data=form, headers=headers, cookies=url_info['cookies'])

    if r.status_code == 200:
        return json.loads(r.text)
    else:
        return False

def create_download_link(download_data):
    try:
        # http://media4.sdarot.pm/watch/480/123927.mp4?token=-_j2UOCoAHr95XJfbKK1Vw&time=1475317746
        return "http://{url}/watch/{watch_n}/{VID}.mp4?token={token}&time={time}".format(
            url=download_data['url'],
            watch_n = download_data['watch'].items()[0][0],
            VID=download_data['VID'],
            token=download_data['watch'].items()[0][1],
            time=download_data['time']
        )
    except:
        return False


def download_url(url, outfile):
    stdout.write('[*] Preparing download... ')
    stdout.flush()
    try:
        r = requests.get(url, stream=True, timeout=30)
    except requests.exceptions.ConnectionError:
        stderr.write('[!] Connection error: {}\n'.format(url))
        stderr.flush()
        return False
    except requests.exceptions.Timeout:
        stderr.write('[!] Connection timeout, please try again later.\n')
        stderr.flush()
        return False

    if r.status_code != 200:
        stderr.write('[!] HTTP error code {}\n'.format(r.status_code))
        stderr.flush()
        return False

    stdout.write('Done!\n')
    stdout.flush()

    # lets download
    file_size = int(r.headers.get('Content-Length', -1))
    fsize_mb = file_size/1024/1024
    chunk_size = 1024
    downloaded_bytes = 0
    update_seconds = 1

    start_timestamp = datetime.now()
    lastupdate = start_timestamp
    try:
        with open(outfile, 'wb') as outf:
            stdout.write('[*] Downloading {fname} [{fsize:.2f}Mb]\n'.format(fname=outfile, fsize = fsize_mb))
            stdout.flush()
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:   # filter out keep-alive new chunks
                    outf.write(chunk)
                    downloaded_bytes += len(chunk)

                    if downloaded_bytes==file_size or (datetime.now() - lastupdate).total_seconds() >= update_seconds:
                        lastupdate = datetime.now()
                        cur_td = (datetime.now() - start_timestamp)

                        stdout.write('\r    {prec} @{kbps:.2f} Kbps ETA: {eta}'.format(
                            kbps = (downloaded_bytes/1024) / cur_td.total_seconds(),
                            prec = '{:.2f}%'.format((downloaded_bytes / file_size)*100) if file_size > 0 else '',
                            eta = timedelta(seconds=((file_size - downloaded_bytes) / (downloaded_bytes / cur_td.total_seconds()))) if file_size > 0 else '--',
                        ))
                        stdout.flush()
            stdout.write('\n')
            stdout.flush()
    except KeyboardInterrupt:
        stdout.write('\nCanceled by user.\n')
        stdout.flush()
        try:
            unlink(outfile)
        except:
            pass
        return False

    stdout.write('\n[*] Download complete, enojoy!\n')
    stdout.flush()
    return True

def banner():
    print "sdarotdl (Version: {0}, {1})".format(VERSION_NUMBER, VERSION_DATE)
    print

def main():
    banner()

    parser = argparse.ArgumentParser(description="Sdarot.pm downloader")
    parser.add_argument('url', action='store', help="URL to download")
    parser.add_argument('-n', '--no-download', action='store_false', default=True, dest='download', help='Do not download, just get video url')
    parser.add_argument('-o', action='store', default='', type=str.strip, help='Set output file name (use without -n)', metavar='file')


    args = parser.parse_args(argv[1:])

    # if not (args.url.startswith('http://www.sdarot.pm/watch/') or args.url.startswith('http://sdarot.pm/watch/')):
    #     stderr.writelines('This is not sdarot.pm url.\nSample url: {}\n'.format(
    #         'http://www.sdarot.pm/watch/82-%D7%9E%D7%A9%D7%97%D7%A7%D7%99-%D7%94%D7%9B%D7%A1-game-of-thrones/season/4/episode/6 \n'))
    #     stderr.flush()
    #     exit(1)

    try:
        print '[*] Preparing to download {url}'.format(url=args.url)
        url_info = get_url_info(args.url)
        stdout.write('[*] Retrieving token... ')
        stdout.flush()
        url_info['token'] = get_token(url_info)

        if not url_info['token']:
            stderr.write('[!] Can\'t get token\n')
            stderr.flush()
            exit(2)
        stdout.write('Done!\n');
        stdout.flush()

        for i in xrange(SECONDS_TO_WAIT):
            stdout.write('\r[*] Waiting {seconds} seconds... '.format(seconds=SECONDS_TO_WAIT-i-1))
            stdout.flush()
            sleep(1)
        stdout.write('Done!\n');
        stdout.flush()

        stdout.write('[*] Retrieving download data... ')
        stdout.flush()
        download_data = get_download_url_data(url_info)

        if not download_data:
            stderr.write('[!] Can\'t get download data\n')
            stderr.flush()
            exit(3)

        download_link = create_download_link(download_data)

        if not download_link:
            stderr.write('Can\'t get download link\n')
            stderr.flush()
            exit(4)

        stdout.write('Done!\n');
        stdout.flush()

        if args.download:
            download_url(download_link, expanduser(args.o) if args.o != '' else url_info['filename'])
        else:
            print "Video url:", download_link

    except KeyboardInterrupt:
        print "Canceled by user"
        exit(0)
    except Exception, ex:
        stderr.write('Error: {}\n'.format(ex))
        stderr.flush()
        exit(99)

if __name__ == '__main__':
    main()