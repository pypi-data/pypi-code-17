from setuptools import setup

setup(name='slackclient-reconnect',
      version='1.0.1',
      description='Python client for Slack.com, with reconnect logic',
      url='https://github.com/btubbs/python-slackclient/tree/ClientReconnect',
      author='Ryan Huber',
      author_email='ryan@slack-corp.com',
      license='MIT',
      packages=['slackclient'],
      install_requires=[
        'websocket-client',
        'requests',
        'six',
      ],
      zip_safe=False)
