import pytest, os, sys

here = os.path.dirname(os.path.abspath(__file__)).lower()

os.chdir('tests')

for p in sys.path.copy():
	if p.lower() == here:
		sys.path.remove(p)
