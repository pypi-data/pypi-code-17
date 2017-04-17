import argparse
from PttWebCrawler import *

def main():
    """The main routine."""
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='''
        A crawler for the web version of PTT, the largest online community in Taiwan.
        Input: board name and page indices (or articla ID)
        Output: BOARD_NAME-START_INDEX-END_INDEX.json (or BOARD_NAME-ID.json)
    ''')
    parser.add_argument('-b', metavar='BOARD_NAME', help='Board name', required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', metavar=('START_INDEX', 'END_INDEX'), type=int, nargs=2, help="Start and end index")
    group.add_argument('-a', metavar='ARTICLE_ID', help="Article ID")

    args = parser.parse_args()
    if args.i != None:
	    PttWebCrawler(board=args.b, iOrA=True, start=args.i[0], end=args.i[1])
    else:
	    PttWebCrawler(board=args.b, iOrA=False, article_id=args.a)

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.

if __name__ == "__main__":
    main()