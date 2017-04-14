import argparse
import logging

from . import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        default=False, help='Enable debugging mode.')
    parser.add_argument('-p', '--port',
                        default=8080, type=int,
                        help='Port to start server on (default: 8080).')
    parser.add_argument('--state', default='.tecthulhu-state',
                        help='Filename to persist tecthulhu state to.')

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARN)
    main(state_filename=args.state, port=args.port, debug=args.debug)
