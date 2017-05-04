import os
from EvoDAG.command_line import CommandLineParams
import gzip
import json
import sys
import logging
from test_command_line import training_set
logging.basicConfig(level=logging.DEBUG)
fname = training_set()


class C(CommandLineParams):
    def parse_args(self):
        self.data = self.parser.parse_args()
        self.data.population_class = 'Generational'
        if hasattr(self.data, 'regressor') and self.data.regressor:
            self.data.classifier = False
        self.main()

sys.argv = ['EvoDAG', '-C', '--parameters',
            'cache.evodag.gz', '-p3', '-e3',
            '-r', '2', fname]
c = C()
c.parse_args()
with gzip.open('cache.evodag.gz') as fpt:
    data = fpt.read()
    try:
        a = json.loads(str(data, encoding='utf-8'))
    except TypeError:
        a = json.loads(data)
a = a[0]
assert 'population_class' in a
assert a['population_class'] == 'Generational'
os.unlink('cache.evodag.gz')
print(a)
