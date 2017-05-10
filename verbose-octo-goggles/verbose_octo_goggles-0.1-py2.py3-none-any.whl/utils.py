import logging


def setup_logger(logger, stream=None, filename=None, fmt=None):
    if len(logger.handlers) < 1:
        if stream:
            console = logging.StreamHandler(stream)
            console.setLevel(logging.DEBUG)
            console.setFormatter(logging.Formatter(fmt))
            logger.addHandler(console)
            logger.setLevel(logging.DEBUG)

        if filename:
            outfile = logging.FileHandler(filename)
            outfile.setLevel(logging.INFO)
            outfile.setFormatter(
                logging.Formatter("%(asctime)s: %(message)s")
            )
            logger.addHandler(outfile)
