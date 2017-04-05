import urllib.request
from ssl import _create_unverified_context


def _url_read(url=None):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, context=_create_unverified_context, timeout=2) as r:
        return _content_decode(r.read())


def _content_decode(content):
    try:
        return content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return content.decode('gbk')
        except UnicodeDecodeError:
            return content.decode('gb2312')


a = [i for i in range(1, 61)]
b = []
for i in a:
    t = 'http://ciee.cau.edu.cn/col/col13728/index.html?uid=21487&pageNum=%s\n' % i
    b.append(t)
with open('1.txt', mode='w') as f:
    f.writelines(b)