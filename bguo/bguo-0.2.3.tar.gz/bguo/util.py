import unicodedata

def as_7bit(x):
    return unicodedata.normalize('NFKD', x) \
        .encode('ascii', 'ignore').decode('utf-8')
