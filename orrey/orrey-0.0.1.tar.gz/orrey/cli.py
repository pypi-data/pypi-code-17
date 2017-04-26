import argparse
import orrey
import sys

#############################
# Create Model Designer     #
#############################
def modelCorrArgs(args):
    parser = argparse.ArgumentParser(
        description='Model Design Correlation Plots')
    parser.add_argument(
        'designfiles', help='Long-form csv model design', nargs='+')
    return parser.parse_args(args)


def modelCorr():
    args = modelCorrArgs(sys.argv[1:])

    mod = orrey.model.ModelWrapper(args.designfiles)
    mod._saveDesign()
    mod._saveFigure()
