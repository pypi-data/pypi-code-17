import sys
from Niff.terminal
from Niff.log import L

def main():
	target = sys.argv[0]
	passwd = sys.argv[1]
	language = sys.argv[2]
	L(target,passwd, language)
