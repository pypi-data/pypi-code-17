#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Api lib for simple life."""
import json
import requests
import uuid

mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]

def tuling(question):
    url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': "fd2a2710a7e01001f97dc3a663603fa1",
        'info': question,
        'userid': mac_address
    }
    try:
        r = json.loads(requests.post(url, data=data).text)
    except:
        return
    if not r['code'] in (100000, 200000, 302000, 308000, 313000, 314000): return
    if r['code'] == 100000: # 文本类
        return '\n'.join([r['text'].replace('<br>','\n')])
    elif r['code'] == 200000: # 链接类
        return '\n'.join([r['text'].replace('<br>','\n'), r['url']])
    elif r['code'] == 302000: # 新闻类
        l = [r['text'].replace('<br>','\n')]
        for n in r['list']: l.append('%s - %s'%(n['article'], n['detailurl']))
        return '\n'.join(l)
    elif r['code'] == 308000: # 菜谱类
        l = [r['text'].replace('<br>','\n')]
        for n in r['list']: l.append('%s - %s'%(n['name'], n['detailurl']))
        return '\n'.join(l)
    elif r['code'] == 313000: # 儿歌类
        return '\n'.join([r['text'].replace('<br>','\n')])
    elif r['code'] == 314000: # 诗词类
        return '\n'.join([r['text'].replace('<br>','\n')])
