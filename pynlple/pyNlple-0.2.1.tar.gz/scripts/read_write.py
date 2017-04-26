# -*- coding: utf-8 -*-
import io

with io.open('../data/youscan/commercial_raw.tsv', 'rt', encoding='utf-8') as source, io.open('../data/youscan/commercial_raw.tsvn', 'wt', encoding='utf-8') as out:
# with io.open('../data/youscan/2017-03-02/104268_autotags.tsvn', 'rt', encoding='utf-8') as source:

    for line in source:
        line = line.strip()
        out.write(line)
        if line.endswith('\tTrue') or line.endswith('\tFalse'):
            out.write('\n')
        else:
            out.write('\\r\\n')
        # if len(line.split('\t')) != 7:
        #     print(line)