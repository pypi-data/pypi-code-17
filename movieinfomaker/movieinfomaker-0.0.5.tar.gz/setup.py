import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='movieinfomaker',
    version = '0.0.5',
    author = 'Anubhab Sen',
    author_email = 'anubhabsen@gmail.com',
    description = 'A script that looks up all movies and TV shows in a folder and gets the  genre, runtime, plot and IMDB and RottenTomatoes ratings of the movie and stores it as a csv file.',
    license = 'BSD',
    keywords = 'movie data info information scrap imdb rottentomatoes',
    url = 'https://github.com/anubhabsen/movie-info',
    packages=['movieinfomaker'],
    long_description=read('README.md'),
    classifiers=[
    ],
)