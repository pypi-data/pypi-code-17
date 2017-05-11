try:
    from zoho import config
    AUTH_TOKEN = config.AUTH_TOKEN
    BASE_HEADERS = config.BASE_HEADERS
except ImportError:
    AUTH_TOKEN = ''
    BASE_HEADERS = {
        'User-Agent': '',
    }
