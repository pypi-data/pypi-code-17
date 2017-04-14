#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Life's pathetic, happy coding ♡~ Nasy.

O._.O
(\=/)

@author: Nasy
@date: Apr 13
@email: sy_n@me.com
@file: cqdb/__init__.py
@license: MIT
@version: 0.0.1

Copyright © 2017 by Nasy. All Rights Reserved.
"""
__version__ = "0.0.3"
import io

import requests as req

try:
    from tqdm import tqdm
except ModuleNotFoundError:

    def tqdm(iter, total=None, unit="MB"):
        """Hand made tqdm."""
        print("Get data: ", end='')
        for i in iter:
            print("#", end='')
            yield i


URL = ("http://192.168.113.12:50075/webhdfs/v1/flume/{date}/{type}/SZ/"
       "{date}01/{code}.csv?op=OPEN&namenoderpcaddress=nameservice1&offset=0")


def gets(date, type, code):
    """Get stream datas."""
    return req.get(URL.format(date=date, type=type, code=code), stream=True)


def get(date, type, code, fm=False, lst=False):
    """Get datas."""
    res = gets(date, type, code)
    content = b""
    for i in tqdm(
            res.iter_content(1024 * 1024),
            total=int(res.headers["Content-Length"]) / (1024 * 1024),
            unit="MB"):
        content += i
    content = content.decode()
    if fm:
        content = io.StringIO(content)
        content = (i.replace("\r\n", "") for i in content)
        if lst:
            content = list(content)
    return content


def main() -> None:
    """Main function for test."""
    pass


if __name__ == "__main__":
    main()
