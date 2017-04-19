from distutils.core import setup

setup(
      name = 'pythinkingcleaner',
      packages = ['pythinkingcleaner'],
      install_requires = ['requests'],
      zip_safe = True,
      license='MIT',
      version = '0.0.3',
      description = 'Library to control ThinkingCleaner devices',
      author = 'Dennis Karpienski',
      author_email = 'dennis@karpienski.de',
      url = 'https://github.com/TheRealLink/pythinkingcleaner',
      download_url = 'https://github.com/TheRealLink/pythinkingcleaner/archive/0.0.3.tar.gz',
      keywords = ['thinkingcleaner', 'roomba'],
      classifiers = [],
)