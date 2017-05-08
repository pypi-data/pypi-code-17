#!/usr/bin/env python3

import argparse
import string

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords as SW

from collections import Counter


NON_WORDS = "”“‘’"

START_OF_GUTENBERG = '*** START OF THIS PROJECT GUTENBERG EBOOK'


def gutenberg_stop_cond(line):
    return line.startswith('End of the Project Gutenberg EBook')


def get_gutenberg_info(fobj):
    info = {
            'name': '',
            'author': '',
            'language': '',
            'source': '',
    }

    if "gutenberg" in fobj.readline().lower():
        for line in fobj:
            if line.startswith('Author: '):
                info['author'] = line.split('Author: ')[1].strip()
            if line.startswith('Title: '):
                info['name'] = line.split('Title: ')[1].strip()
            if line.startswith('Language: '):
                info['language'] = line.split('Language: ')[1].strip()
            # Ebook #NUMBER, but as we don't know EBook or Ebook used
            # convert all to lower case is expensive
            if 'ook #' in line:
                gid = line.strip().split("#")[1].strip(']')
                info['source'] = 'http://www.gutenberg.org/ebooks/{0}'.format(gid)  # NOQA

            if line.startswith(START_OF_GUTENBERG):
                # When reach here, the text is iterated
                # to the content in Gutenberg
                break
    else:
        fobj.seek(0, 0)

    return info


def tokenize(sentences):
    assert isinstance(sentences, str)
    words = (w.strip(NON_WORDS + string.punctuation)
             for w in word_tokenize(sentences))
    return filter(None, words)


def count(fobj, stop_word=True,
          stop_cond=None,
          with_example=True):
    '''
    counts frequency of words, return the most-used words
    and sentences which they appear.
    '''
    counter = Counter()
    word_sentences = {}
    for line in fobj:
        if stop_cond is not None and stop_cond(line):
            break
        sentences = line.split('.')
        # normalize all begin sentence words
        for s in sentences:
            s = s.strip()
            if len(s) == 0:
                continue
            words = [w.lower() for w in tokenize(s)]
            if with_example:
                for w in words:
                    if w not in word_sentences:
                        word_sentences[w] = s
            counter.update(words)

    _will_remove_stop_words = not stop_word
    counter = remove(counter, NON_WORDS, stop_word=_will_remove_stop_words)
    return (counter, word_sentences)


def remove(counter, custom=None, stop_word=True):

    toremove = []
    if stop_word:
        toremove.extend(SW.words('english'))

    if custom:
        toremove.extend(custom)

    for w in toremove:
        try:
            counter.pop(w)
        except KeyError:
            pass
    return counter


def _print_top(counter, sentences=None, n=100, with_example=False):
    '''
    Storing all sentences where each word appear is expensive.
    with_example allows print out the first sentence each word appear.
    '''
    FMT = '{order:>4}. {freq:<5} {word:<20}'
    EG = ' ' * 20 + 'E.g: {sentence}'
    most = counter.most_common(n)
    for idx, (word, freq) in enumerate(most, start=1):
        print(FMT.format(order=idx, freq=freq, word=word))
        if with_example:
            print(EG.format(sentence=sentences[word]))


def cli():
    argp = argparse.ArgumentParser()
    argp.add_argument('file', help='Text file to analyse')
    argp.add_argument('--stop-words', '-s', help='Count stop-words',
                      action='store_true', default=False)
    args = argp.parse_args()
    with open(args.file) as f:

        info = get_gutenberg_info(f)
        print('Getting top words for {name} by {author} in language {language} {source}'.format(**info))  # NOQA
        print('Next line {}'.format(f.readline()))

        counter, sentences = count(f, stop_word=args.stop_words,
                                   stop_cond=gutenberg_stop_cond)
        _print_top(counter, sentences, with_example=True)


if __name__ == "__main__":
    cli()
