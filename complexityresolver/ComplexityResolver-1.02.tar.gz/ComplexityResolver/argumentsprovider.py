import argparse
import exceptions
import consts


class ArgumentsProvider:
    def __init__(self):

        self.parser = argparse.ArgumentParser()
        # Adding command line arguments to parser
        self.parser.add_argument(
            '--timeout',
            help="""Time in seconds, after witch
 program will stop trying to compute result""",
            type=int,
            default=30)
        self.parser.add_argument(
            '--samplingFrom',
            help='Size of N, from witch algorithm will start sampling',
            type=int,
            default=consts.START_SAMPLING_SIZE)
        self.parser.add_argument(
            '--samplingTo',
            help='Size of N, till witch algorithm will try to do sampling',
            type=int,
            default=consts.SAMPLING_END)

    def validate_arguments(self):
        args = self.parser.parse_args()
        if args.timeout <= 0:
            raise exceptions.ArgumentException(
                "Parameter 'timeout' could not be less than 1")

        if args.samplingFrom >= args.samplingTo:
            raise exceptions.ArgumentException(
                "Parameter samplingTo must be greater than samplingFrom")

        if args.samplingFrom <= 0:
            raise exceptions.ArgumentException(
                "Parameters samplingFrom & samplingTo must be greater than 0")

        return args
