import logging
import time
from typing import List

from cassandra.cluster import (Cluster,
                               NoHostAvailable)

logger = logging.getLogger(__name__)


def check_connection(*,
                     contact_points: List[str],
                     port: int,
                     retry_interval: int = 5,
                     attempts_count: int = 12):
    for attempt_num in range(attempts_count):
        try:
            with Cluster(contact_points=contact_points,
                         port=port) as cluster:
                cluster.connect()
            break
        except NoHostAvailable:
            err_msg = ('Connection attempt '
                       f'#{attempt_num + 1} failed.')
            logger.error(err_msg)
            time.sleep(retry_interval)
    else:
        err_message = ('Failed to establish connection '
                       f'with "{contact_points}" '
                       f'after {attempts_count} attempts '
                       f'with {retry_interval} s. interval.')
        raise ConnectionError(err_message)
    return cluster
