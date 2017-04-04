


import argparse


def parse_cli() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument('--universe-size', '-u', nargs=2, metavar=('W', 'H'),
                        type=int, default=(600, 600),
                        help="size of universe/window.")
    parser.add_argument('--padding', '-p', type=int, default=50,
                        help="space between triangulation and window border.")
    parser.add_argument('--fps', '-f', type=int, default=10,
                        help="frame per second.")
    parser.add_argument('--speed', '-s', type=float, default=0.01,
                        help="Time between ticks.")
    parser.add_argument('--mouse_precision', '-m', type=int, default=400,
                        help="Click detection precision.")
    return dict(parser.parse_args()._get_kwargs())


if __name__ == "__main__":
    from pydelaunator import gui
    gui.run(**parse_cli())
