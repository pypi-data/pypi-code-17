from setuptools import setup

with open('./README.md') as f:
    long_desc = f.read()

setup(
  name = 'S3toECS', 
  version = '0.0.1',
  description = 'Tool that transfer Docker images from S3 to your ECS repository.',
  long_desc = long_desc,
  author = 'Antonio Maiolo',
  author_email = 'maiolo.antonio@territory.de',
  license = 'MIT License',
  url = 'https://github.com/territory-webguerillas/s3toecs/',
  download_url = 'https://github.com/territory-webguerillas/s3toecs/archive/0.1.1.tar.gz', 
  keywords = ['s3', 'ecs', 'aws', 's3 to ecs'],
  entry_points = {
        'console_scripts': [
            's3toecs = s3toecs:main'
        ]
  },
  classifiers = [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
  ],
)
