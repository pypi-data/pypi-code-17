#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import ujson
# from .config import config
# import gmfun
import time
from .gmfun import gmfun

def query_userinfo(mysess, userid=None, role=None, item=None, style='fq'):
    """ 查询用户信息
    item 查询项目
    """
    req = {'mysess': mysess,
           'style': style}
    if item:
        req.update({'where': ','.join(item)})
    if userid:
        req.update({'userid': userid,
                    'role': role})
    data = gmfun.send_then_wait('hy_load_userinfo_by_where', req)
    if data and data.get('status', 0) == 200:
        data = data.get('body')
        return data


def query_userinfo_lst(mysess, uid_role_lst, item=None):
    """ 查询用户信息list方法
    item 查询项目
    """
    req = {'mysess': mysess,
           'uid_role_lst': uid_role_lst}
    if item:
        req.update({'where': ','.join(item)})

    data = gmfun.send_then_wait('hy_load_userinfo_by_userid_lst', req)
    if data and data.get('status', 0) == 200:
        data = data.get('body')
        return data


def query_user_tags(mysess, userid=None, role=None):
    """ 查询用户标签
    """
    req = {'mysess': mysess
           }

    if userid:
        req.update(
            {'userid': userid,
             'role': role})
    data = gmfun.send_then_wait('hy_load_user_lable_by_id', req)
    if data and data.get('status', 0) == 200:
        data = data.get('body')
        return data


def query_colleagues_info(mysess, userid=None, role=None, item=None, gift=None, keywords=None, **kw):
    """ 查询同事信息
    :mysess:
    """
    req = {'mysess': mysess}
    req.update(kw)

    if keywords:
        req.update({'keywords': keywords})

    if item:
        req.update({'where': ','.join(item)})

    if gift:
        req.update(gift)

    if userid:
        req.update({'userid': userid,
                    'role': role})

    data = gmfun.send_then_wait('hy_load_list_of_colleagues', req)
    if data and int(data.get('status', 0)) == 200:
        data_list = data.get('body', {}).get('user_lst', [])
        [x.update({'u_type': 'c'}) for x in data_list]
    else:
        data_list = []
        # [
        #   {u'grp_id': u'', u'_id': 50094, u'm': 1472009834834L, u'id': u'50094', u'park_id': u''},
        #   {u'grp_id': u'', u'_id': 77730, u'm': 1471506018712L, u'id': u'77730', u'park_id': u''},
        #   {u'grp_id': u'', u'_id': 70683, u'm': 1471497971318L, u'id': u'70683', u'park_id': u''},
        #   {u'grp_id': u'', u'_id': 45830, u'm': 1471417614953L, u'id': u'45830', u'park_id': u''},
        #   {u'grp_id': u'', u'_id': 95345, u'm': 1471416269490L, u'id': u'95345', u'park_id': u''},
        #   {u'grp_id': u'', u'_id': 23464, u'm': 1471413400914L, u'id': u'23464', u'park_id': u''}
        # ]
    return data_list


def now_time():
    """ 当前UTC时间戳
    """
    return int(time.time() * 1000)
