import sys
from Niff.terminal import ranger
from Niff.log import L

def main():
	target = sys.argv[1]
	passwd = sys.argv[2]
	language = sys.argv[3]
	L(target,passwd, language)
	ranger(target, passwd, language)
