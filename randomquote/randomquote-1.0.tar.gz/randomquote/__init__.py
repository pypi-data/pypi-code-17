from urllib.request import urlopen
import urllib
import json
from bs4 import BeautifulSoup

def GetQuote():
    url = 'http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1'
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            }

    request = urllib.request.Request(url, headers=headers)
    connection = urllib.request.urlopen(request)
    response = connection.read()

    data = json.loads(response)

    quote = BeautifulSoup(data[0]["content"], 'html.parser').get_text()
    quote = quote.replace('\n', '')
    quote = quote.strip()
    author = BeautifulSoup(data[0]["title"], 'html.parser').get_text()
    author = author.replace('\n', '')
    author = author.strip()

    final_text = "{} ~{}".format(quote, author)

    return final_text

