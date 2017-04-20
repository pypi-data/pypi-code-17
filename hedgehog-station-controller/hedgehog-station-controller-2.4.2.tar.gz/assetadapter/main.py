import argparse
import logging

from rpc.server import VisaRpcServer

def main():
    ## Parse command line arguments.
    parser = argparse.ArgumentParser()

    parser.add_argument("-H", "--host", help="Automation server host of field agent.", type=str, default='localhost')
    parser.add_argument("-V", "--backend", help="PyVISA backend.", type=str, default='test.yml@sim')
    parser.add_argument("-e", "--exchange", help="RabbitMQ exchange for RPC.", type=str, default='visa_rpc')
    parser.add_argument("-u", "--username", help="RabbitMQ username.", type=str, default='guest')
    parser.add_argument("-P", "--port", help="RabbitMQ port.", type=int, default=5672)
    parser.add_argument("-p", "--password", help="RabbitMQ password.", type=str, default='guest')
    parser.add_argument("-v", "--verbose", help="Increase output verbosity.", action="store_true")
    parser.add_argument("-l", "--logfile", help="Logging to file.", type=str, default="/opt/hedgehog-station-controller/output.log")

    args = parser.parse_args()

    rootlogger = logging.getLogger('root')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this fo
    console.setFormatter(formatter)
    # add the handler to the root logger
    rootlogger.addHandler(console)

    logger = logging.getLogger('assetadapter.main')
    logfile = logging.FileHandler(args.logfile)
    logfile.setLevel(logging.DEBUG)
    # set a format which is simpler for console use
    logfile_formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    # tell the handler to use this fo
    logfile.setFormatter(logfile_formatter)
    # add the handler to the root logger
    logger.addHandler(logfile)

    logger.setLevel(logging.DEBUG)

    logger.info("Initialize controller service with configuration: " + str(args))

    # Initialize VISA RPC server
    server = VisaRpcServer(
        logger=logger,
        host=args.host,
        username=args.username,
        password=args.password,
        visa_library=args.backend,
        exchange=args.exchange
    )

    server.start()


