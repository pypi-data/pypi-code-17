#! /usr/bin/env python3


from pycliprog import Prog, ExitFailure


class TestProg(Prog):
    def main(self):
        if self.args.fail:
            raise ExitFailure('Something bad happened!')
        print('Everything is operational!')

    def add_args(self):
        self.parser.add_argument('-f', '--fail',
                                 action='store_true',
                                 help='Fail.')


if __name__ == '__main__':
    TestProg().start()
