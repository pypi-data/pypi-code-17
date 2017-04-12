import sys
import requests
from stepist.flow import step, run, factory_step

URLS = ['https://www.python.org/',
        'https://wikipedia.org/wiki/Python_(programming_language)']


@step(None)
def step3(text, **kwargs):
    c = text.count('python')
    return c


@factory_step(step3, as_worker=True)
def step2(url):
    r = requests.get(url)
    return dict(url=url,
                text=r.text)


@step(None, next_flow=step2)
def step1(urls, next_flow):
    for url in urls:
        next_flow.add_item(dict(url=url))

    return list(next_flow.result())


if sys.argv[1] == "worker":
    run(step2)  # run worker
else:
    print(step1(urls=URLS))
