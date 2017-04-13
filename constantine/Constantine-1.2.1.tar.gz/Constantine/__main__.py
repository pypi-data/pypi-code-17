import sys
from Constantine import main

def execute(args=None):

    if args is None:
        args = sys.argv
        main.run(args)

if __name__ == "__main__":
    execute()
