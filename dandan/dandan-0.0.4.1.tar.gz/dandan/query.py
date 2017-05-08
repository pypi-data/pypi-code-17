def local_ip():
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
    import value
    import requests

    kwargs = value.AttrDict(kwargs)
    timeout = 60
    if kwargs.timeout:
        timeout = kwargs.timeout

    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"

    if kwargs.headers:
        headers = kwargs.headers
    else:
        headers = value.AttrDict()

    if not headers["User-Agent"]:
        headers["User-Agent"] = user_agent

    try:
        res = requests.get(url, timeout=timeout, headers=headers)
    except Exception:
        return None

    return res.text


def soup(url, **kwargs):
    from bs4 import BeautifulSoup as bs

    text = html(url, **kwargs)
    if not text:
        return None

    soup = bs(text, "html.parser")
    return soup


def whois(address):
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
