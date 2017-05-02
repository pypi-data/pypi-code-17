import os

WORDS_DIR = os.path.dirname(os.path.realpath(__file__))
FILENAME = 'words.txt'
FILE_PATH = os.path.join(WORDS_DIR, FILENAME)


class PatoisStopWordsError(Exception):
    pass


def get_patois_stop_words():
    try:
        with open(FILE_PATH, 'rb') as words_file:
            stop_words = [line.decode('utf-8').strip()
                          for line in words_file.readlines()]
    except IOError:
        raise PatoisStopWordsError(
            'Couldn\'t read {0}, check whether it has been removed or modified.'.format(FILE_PATH))

    return stop_words
