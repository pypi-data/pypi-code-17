from setuptools import setup, find_packages

setup(
    name = 'kli', 
    version = '0.0.5', 
    include_package_data = True,
    py_modules = ['main', 'classes', 'support', 'imports'],
    license = 'MIT',
    url = 'https://github.com/tranquilo12/kl',
    author = 'Shriram Sunder',
    author_email = 'shriram.sunder121091@gmail.com',
    install_requires = [
        'tqdm', 
        'pprint',
        'argcomplete',
        'bs4', 
        'click>=6', 
        'cryptography'
        ],    
    entry_points = '''
        [console_scripts]
        kli=main:kli
    ''',
    data_files=[('', ['comp.json']),
                ('', ['keys.txt'])]
        )
