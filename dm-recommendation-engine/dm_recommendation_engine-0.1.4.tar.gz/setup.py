from distutils.core import setup

setup(
    name='dm_recommendation_engine',
    version='0.1.4',
    packages=['dm_recommendation_engine'],
    url='https://github.com/DiscoverMovies/recommendation_engine',
    license="MIT License",
    author='Sidhin S Thomas',
    author_email='sidhin.thomas@gmail.com',
    description="Module used by discover movies to generate recommendations", requires=['sklearn', 'pandas']
)