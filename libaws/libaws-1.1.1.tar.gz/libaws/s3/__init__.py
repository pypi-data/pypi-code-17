from libaws.common.logger import logger

def daemonize():
    try:
        from libaws.base import daemon
        daemon.daemonize()
    except Exception,e:
        logger.warn('%s',e)

