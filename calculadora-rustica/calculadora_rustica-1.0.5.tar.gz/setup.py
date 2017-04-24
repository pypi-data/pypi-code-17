'''
* setup.py
*
* Configuracao de aspectos do projeto.
* Interface da linha de comando para executar tarefas relacionadas ao empacotamento
     * exemplo: listagem dos comandos possiveis (help).
'''

# import do find_packages
from setuptools import setup, find_packages

# import open e path
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Pegar 'long description' do arquivo README
try:
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = ' '


setup(

    # nome do projeto
    name = 'calculadora_rustica',

    # versao atual do projeto
    version = '1.0.5',

    # descricao curta sobre o projeto
    description = 'This is a project test',
    # descricao longa sobre o projeto
    long_description = long_description,

    # endereco do projeto
    url = 'https://github.com/JaineBudke/BIOME_testes_calcrustica.git',

    # detalhes sobre o autor
    author='Jaine Budke',
    author_email='jainebudke@hotmail.com',

    # tipo de licenca que esta sendo utilizada
    license='MIT',

    # classificadores que caracterizam o projeto
    classifiers = [

        # maturidade do projeto
        'Development Status :: 1 - Planning',

        # publico alvo do projeto
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',

        # licenca utilizada
        'License :: OSI Approved :: Academic Free License (AFL)',

        # versao python suportada
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'

    ],

    # descricao com palavras-chaves
    keywords='bioinformatics neuroscience teste',

    # lista de pacotes que devem ser incluidos no projeto
    # find_packages os encontra automaticamente
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # lista de dependencias que o projeto minimamente precisa ter para ser executado
    install_requires=['sh>=1.11',
                                'numpy>=1.12',
                                'scipy>=0.19'],

)