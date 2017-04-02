from random import randint

facts = ['He is an engineering undergraduate.',
         'He is a huge fan of Game of Thrones.',
         'He tries to make sure that things are symmetrical (when it comes to arrangement and organizing stuff).',
         'He hates people who don\'t indent their code properly.',
         'He is a lover of open source.',
         'A good internet connection and pizza is all he needs.',
         'He is excited about Google Summer of Code.',
         'He is an enthusiastic developer and lover of learning new things.',
         'He is playing Dota 2.',
         'He is interested in Machine Learning']

def says():
    print (facts[randint(0,9)])
