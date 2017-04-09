from setuptools import setup

setup(name='nephelo',
      version='0.101',
      description='A Cloud Formation library to more easily. Nephelo, short for Nephelococcygia, is the art of watching clouds.',
      url='https://github.com/tamme-io/nephelo',
      author='tamme',
      author_email='opensource@tamme.io',
      license='MIT',
      packages=[
            'nephelo'
      ],
      install_requires=[
            'boto3',
            'netaddr'
      ],
      include_package_data=True,
      package_data={
            'templates': [
                  'templates/vpc.json',
                  'templates/subnet.json'
            ]
      },
      scripts=['bin/nephelo'],
      zip_safe=False)