import sys
import requests
from stepist.flow import step, run, factory_step

URLS = ['https://www.python.org/',
        'https://wikipedia.org/wiki/Python_(programming_language)']


@step(None)
def step3(text, **kwargs):
    print(text.count('python'))


@factory_step(step3, as_worker=True)
def step2(url):
    r = requests.get(url)
    return dict(url=url,
                text=r.text)


@step(step2)
def step1(urls):
    print("urls")
    return [dict(url=url) for url in urls]


if sys.argv[1] == "worker":
    run(step2)  # run worker
else:
    print(step1(urls=URLS))
