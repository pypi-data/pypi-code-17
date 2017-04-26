# -*- coding: utf-8 -*-
import logging
import re

from pynlple.data.corpus import StackingSource, FilteringSource, JsonFieldSource, MappingSource, \
    OpensubtitlesSentenceSource, FileLineSource
from pynlple.data.filesource import FilePathSource
from pynlple.data.jsonsource import FileJsonDataSource
from pynlple.processing.preprocessor import DefaultPreprocessorStack, RegexReplacerAdapter
from pynlple.module import abs_path, append_paths
from gensim.models import Phrases

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

replacers_stack = DefaultPreprocessorStack()

path1 = 'F:/text_lang/'
path2 = 'F:/data/youscan/mentions/2016.12.09-I_lang/'
path3 = 'F:/data/youscan/mentions/2016.12.09-II_lang/'
path4 = 'F:/data/youscan/mentions/2016.12.09-III_lang/'

facebook_looksmi_source = StackingSource([FileJsonDataSource(path) for path in FilePathSource([path1])])
language_facebook_looksmi_source = FilteringSource(facebook_looksmi_source, lambda j: j['lang'] in ['rus'])
text_facebook_looksmi_source = JsonFieldSource(language_facebook_looksmi_source, 'Text')

youscan_source = StackingSource([FileJsonDataSource(path) for path in FilePathSource([path2, path3, path4])])
language_youscan_source = FilteringSource(youscan_source, lambda j: j['lang'] in ['rus'])
text_youscan_source = JsonFieldSource(youscan_source, 'text')

opensub_file = 'F:/corpora/OpenSubtitles/OpenSubtitles2016.raw.ru'
dash_cleaner = RegexReplacerAdapter(r'(^-\s)|(-+$)', '', False, False, False)
opensub_sentences = OpensubtitlesSentenceSource(MappingSource(FileLineSource(opensub_file, encoding='utf-8'), dash_cleaner.preprocess))

all_text_source = StackingSource([text_facebook_looksmi_source, text_youscan_source, opensub_sentences])

line_pattern = re.compile(r'[\r\n]+')
line_source = StackingSource(MappingSource(all_text_source, lambda t: line_pattern.split(t)))
token_source = MappingSource(line_source, lambda t: replacers_stack.preprocess(t).split())

# one_file_path1 = 'F:/text_lang/facebook-text-1.txt'
# one_file_source = FileJsonDataSource(one_file_path1)
# language_one_file_source = FilteringSource(one_file_source, lambda j: j['lang'] in ['rus'])
# text_one_file__source = JsonFieldSource(language_one_file_source, 'Text')
# line_source = StackingSource(MappingSource(text_one_file__source, lambda t: re.split(r'[\r\n]+', t)))
# token_source = MappingSource(line_source, lambda t: replacers_stack.preprocess(t).split())

n = 2
source = FilteringSource(token_source, lambda s: len(s) >= n)

key = 'rus_OS_min_tokens=' + str(n)
pars = dict(
    min_count=5,
    threshold=10,
    max_vocab_size=50000000,
    delimiter=b'+',
)
params = '_'.join(repr(key) + '=' + repr(pars[key]) for key in sorted(pars.keys()))
# vocab_name = 'gensim_phrases_' + key + '_' + params + '.vcb'
# vocab_path = append_paths(abs_path('model/'), vocab_name)
model_name = 'gensim_phrases_' + key + '_' + params + '.tst'
model_path = append_paths(abs_path('model/'), model_name)

pars['progress_per'] = 100000
model = Phrases(source, **pars)
print('First training step finished.')
model.save(model_path)

model = Phrases.load(model_path)
print('Model ' + model_name + ' was successfully loaded.')

print(model.export_phrases(['С утра съел кит кат и эм энд эмс и неплохо себя чувствую .'.split()]))



