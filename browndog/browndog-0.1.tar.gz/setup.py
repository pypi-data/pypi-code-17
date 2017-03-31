from distutils.core import setup
setup(
  name = 'browndog',
  packages = ['browndog'], # this must be the same as the name above
  version = '0.1',
  description = '''Researchers in these disciplines sometimes require to work with or to explore their difficult 
    datasets. For ease of the researchers, we built a Python library that wraps Brown Dog REST API and provides 
    modules to identify the conversion options for a file/dataset, to convert file/dataset to appropriate 
    format.  Towards this they could leverage the Brown Dog Services (DAP/DTS). For ease of the researchers, 
    we built a Python library that wraps Brown Dog REST API and provides modules to identify the conversion 
    options for a file/dataset, to convert file/dataset to appropriate format, to index collections and to 
    query collections. This Python library can also be easily integrated with other statistical software written 
    in R. So, the researcher need not require learning a new programming language and prior knowledge of Python 
    is sufficient to use Brown Dog services.''',
  author = 'Kenton McHenry',
  author_email = 'browndog-support@ncsa.illinois.edu',
  url = 'https://github.com/NCSABrownDog/bd.py', 
  download_url = 'https://github.com/NCSABrownDog/bd.py',
  keywords = ['Browndog'],
  classifiers = []
)