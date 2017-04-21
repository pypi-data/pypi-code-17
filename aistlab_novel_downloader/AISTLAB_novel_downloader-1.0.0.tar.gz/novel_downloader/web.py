# -*- coding:utf-8 -*-
# from novel_grab import novel_grab
from flask import Flask, request, render_template
import threading
import json
import urllib.request, urllib.error
import os, sys
import queue

from novel_grab.novel_grab import Downloader

app = Flask(__name__, static_url_path="")  # omit static

with open(os.path.join(sys.path[0], 'novels.json'), 'r', encoding='utf-8') as gf:  # relative path
    novels = json.load(gf)


def index_novel(u):
    for i, m in enumerate(novels):
        if m["from"] == u:
            return i
    return -1


def add_item(n, f, d):
    id = index_novel(f)
    if id < 0:
        novels.append({"id": len(novels) + 1, "name": n, "from": f, "state": 0, "download": d})
        return True, len(novels) - 1
    else:
        return False, id


@app.route('/update')
def update():
    for g in grab_list:
        novels[g.info["id"]]['state'] = "%d" % g.get_info()["percent"]
        if g.get_info()["percent"] == 100:
            with open(os.path.join(sys.path[0], 'novels.json'), 'w', encoding='utf-8') as outfile:
                json.dump(novels, outfile)
            grab_list.remove(g)
    return json.dumps(novels)


grab = Downloader()
grab_list = []


@app.route('/')
def index():
    global grab
    url = request.query_string.decode('utf8')
    print(url)
    if not str(url).startswith('http'):
        url = "http://" + url
    try:
        urllib.request.urlopen(url, timeout=1000)
    except urllib.error.URLError or urllib.error.HTTPError as e:
        return render_template('index.html', url=url, sites=grab.get_info()["supported_sites"], urlerror=str(e.reason))
    if not grab.set_url(url):
        return render_template('index.html', url=url, sites=grab.get_info()["supported_sites"], urlerror="页面地址并非全部章节页面")
    nid = index_novel(url)
    if nid < 0:  # first add
        grab.start()
        grab_list.append(grab)
        _, grab.info["id"] = add_item(n=grab.get_info()["novel_name"], f=url, d=grab.get_info()["file_name"])
        return render_template('index.html', sites=grab.get_info()["supported_sites"],
                               name=grab.get_info()["novel_name"], url=url, novels=novels)
    else:

        return render_template('index.html', alreadyid=nid + 1, sites=grab.get_info()["supported_sites"],
                               name=grab.get_info()["novel_name"], url=url, novels=novels)
    return "invalid."


def main():
    """
    insert localhost:777?   before your novel chapters index page.
    """
    os.chdir(os.path.join(sys.path[0], "static"))  # switch for download
    app.run(host='0.0.0.0', debug=True, port=777)  # todo 生产环境运行


if __name__ == '__main__':
    main()
