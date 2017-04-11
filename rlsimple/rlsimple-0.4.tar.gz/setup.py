from distutils.core import setup
setup(
  name = 'rlsimple',
  packages = ['rlsimple'], # this must be the same as the name above
  version = '0.4',
  description = 'reinforcement learning simple library',
  author = 'Rabbit Noname',
  author_email = 'faithoptimistic@gmail.com',
  url = 'https://github.com/rabbitnoname/rlsimple', # use the URL to the github repo
  download_url = 'https://github.com/rabbitnoname/rlsimple/archive/master.zip', # I'll explain this in a second
  keywords = ['reinforcement learning', 'DDPG', 'DQN', 'Actor Critic', 'simple library'], # arbitrary keywords
  classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ]
)
