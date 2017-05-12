def local_ip():
    '''get local ip address'''

    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def html(url, **kwargs):
    '''get BeautifulSoup object by url

        kwargs:

            timeout : set get timeout default 60
            retry: set retry count default 0
            headers: set http headers

        notice:
            default User-Agent : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"
    '''

    import value
    import requests

    kwargs = value.AttrDict(kwargs)
    timeout = kwargs.timeout or 60
    headers = kwargs.headers or value.AttrDict()
    retry = kwargs.retry or 0

    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"
    headers["User-Agent"] = headers["User-Agent"] or user_agent

    for _ in range(0, retry + 1):
        try:
            return requests.get(url, timeout=timeout, headers=headers).text
        except Exception:
            continue

    return None


def soup(url, **kwargs):
    '''get BeautifulSoup object by url'''

    from bs4 import BeautifulSoup as bs
    text = html(url, **kwargs) or ""
    return bs(text, "html.parser")


def whois(address):
    '''get whois infommation (developing)'''

    import value
    import requests
    result = value.AttrDict()
    result.address = address

    api = "https://wq.apnic.net/whois-search/query"
    params = {
        "searchtext": address,
    }
    try:
        res = requests.get(api, params=params, timeout=5)
        items = res.json()
    except Exception:
        return result

    result.comments = []
    result.objects = []
    for item in items:
        item = value.AttrDict(**item)
        if item.type == "comments":
            result.comments.append(item)
        else:
            result.objects.append(item)
    return result
