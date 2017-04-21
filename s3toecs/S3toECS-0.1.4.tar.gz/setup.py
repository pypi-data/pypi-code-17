from setuptools import setup

setup(
  name = 'S3toECS', 
  version = '0.1.4',
  description = 'Tool that transfers Docker images from S3 to your ECS repository.',
  author = 'Antonio Maiolo',
  author_email = 'maiolo.antonio@territory.de',
  license = 'MIT License',
  url = 'https://github.com/territory-webguerillas/s3toecs/',
  download_url = 'https://github.com/territory-webguerillas/s3toecs/archive/0.1.4.tar.gz', 
  keywords = ['s3', 'ecs', 'aws', 's3 to ecs'],
  python_requires='>=3.6',
  py_modules=['s3toecs'],
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
