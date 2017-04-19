from setuptools import setup


setup(
    name='rl_wsd_labeled',
    version='0.0.2',
    packages=['rl_wsd_labeled'],
    zip_safe=False,
    package_data={
        'rl_wsd_labeled': [
            'verbs/*/*.txt',
            'nouns/*/*.txt',
        ],
    },
)
