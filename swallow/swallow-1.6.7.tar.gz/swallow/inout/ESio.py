from swallow.settings import logger
from elasticsearch import Elasticsearch, helpers, RequestsHttpConnection
import json
import time
from swallow.logger_mp import get_logger_mp

class MyConnection(RequestsHttpConnection):
    def __init__(self, *args, **kwargs):
        proxies = kwargs.pop('proxies', {})
        super(MyConnection, self).__init__(*args, **kwargs)
        self.session.proxies = proxies

class ESio:
    """Reads and Writes documents from/to elasticsearch"""

    def __init__(self, p_host, p_port, p_bulksize, p_proxy=None):
        """Class creation

            p_host:     Elasticsearch Server address
            p_port:        Elasticsearch Server port
            p_bulksize:    Number of doc to index in a time
        """
        self.host = p_host
        self.port = p_port
        self.bulk_size = p_bulksize
        self.scroll_docs = None
        self.proxy = p_proxy

    def count(self, p_index, p_query={}):
        """Gets the number of docs for a query

            p_index:    elasticsearch index where to query
            p_query:    the query to process

            return the number of docs from the index p_index and the query p_query
        """
        try:
            param = [{'host': self.host, 'port': self.port}]
            if self.proxy is None:
                es = Elasticsearch(param)
            else:
                es = Elasticsearch(param, connection_class=MyConnection, proxies={'http': self.proxy})

            logger.info('Connected to ES Server: %s', json.dumps(param))
        except Exception as e:
            logger.error('Connection failed to ES Server : %s', json.dumps(param))
            logger.error(e)

        try:
            result = es.count(index=p_index, body=p_query)
            logger.info('Count the number of items from %s for the query %s', p_index, p_query)
        except Exception as e:
            logger.error('Error querying the index %s with query %s', p_index, p_query)
            logger.error(e)

        return result['count']

    def set_mapping(self, p_index, p_mapping):
        """Create an index with a given p_mapping

            - p_index:     index to delete
            - p_mapping:   mapping forced
        """
        try:
            param = [{'host': self.host, 'port': self.port}]
            if self.proxy is None:
                es = Elasticsearch(param)
            else:
                es = Elasticsearch(param, connection_class=MyConnection, proxies={'http': self.proxy})
            logger.info('Connected to ES Server: %s', json.dumps(param))
        except Exception as e:
            logger.error('Connection failed to ES Server : %s', json.dumps(param))
            logger.error(e)

        try:
            es.indices.create(index=p_index, body=p_mapping)
            logger.info('Index %s created', p_index)
        except Exception as e:
            logger.error('Error creating the index %s', p_index)
            logger.error(e)

    def clear_index(self, p_index):
        """Deletes and index

            - p_index:     index to delete
            - returns true if p_index has been deleted, false if not
        """
        delete_ok = True

        try:
            param = [{'host': self.host, 'port': self.port}]
            if self.proxy is None:
                es = Elasticsearch(param)
            else:
                es = Elasticsearch(param, connection_class=MyConnection, proxies={'http': self.proxy})
            logger.info('Connected to ES Server: %s', json.dumps(param))
        except Exception as e:
            logger.error('Connection failed to ES Server : %s', json.dumps(param))
            logger.error(e)
            delete_ok = False

        try:
            es.indices.delete(index=p_index)
            logger.info('Index %s deleted', p_index)
        except Exception as e:
            logger.error('Error deleting the index %s', p_index)
            logger.error(e)
            delete_ok = False

        return delete_ok

    def dequeue_and_store(self, p_queue, p_index, p_timeout=10, p_nbmax_retry=3, p_disable_indexing=False):
        """Gets docs from p_queue and stores them in the csv file
             Stops dealing with the queue when receiving a "None" item

            p_queue:            queue wich items are picked from. Elements has to be "list".
            p_index:            elasticsearch index where to store the docs
            p_timeout:          timeout for bulk (default is 10s)
            p_nbmax_retry:      number of tries when failing on a request (default is 3)
        """
        logger_mp = get_logger_mp(__name__, self.log_queue, self.log_level, self.formatter)

        es = None
        try:
            param = [{'host': self.host, 'port': self.port, 'timeout': p_timeout, 'max_retries': p_nbmax_retry, 'retry_on_timeout': True}]
            if self.proxy is None:
                es = Elasticsearch(param)
            else:
                es = Elasticsearch(param, connection_class=MyConnection, proxies={'http': self.proxy})
            es.ping()
            logger_mp.info('Connected to ES Server: %s', json.dumps(param))
        except Exception as e:
            logger_mp.error('Connection failed to ES Server : %s', json.dumps(param))
            logger_mp.error(e)

        # We need to record the previous setting, so as to apply it again after bulk operations
        current_settings = {}
        try:
            current_settings = es.indices.get_settings(index=p_index)
            logger_mp.info('Connected to ES Server: %s', json.dumps(param))
        except Exception as e:
            logger_mp.error('Connection failed to ES Server : %s', json.dumps(param))
            logger_mp.error(e)

        if p_disable_indexing:
            try:
                self._disable_indexing_and_replicat(logger_mp, es, p_index)
            except Exception as e:
                logger_mp.error("Can't disable indexing and replicat on {}".format(p_index))
                logger_mp.error(e)

        # Loop untill receiving the "poison pill" item (meaning : no more element to read)
        # Main loop max retry
        main_loop_max_retry = 5
        main_loop_retry = 0
        start = time.time()
        poison_pill = False
        while not(poison_pill):
            try:
                bulk = []
                while (len(bulk) < self.bulk_size):
                    source_doc = p_queue.get()

                    # Manage poison pill
                    if source_doc is None:
                        poison_pill = True
                        p_queue.task_done()
                        break

                    # Bulk element creation from the source_doc
                    source_doc['_index'] = p_index

                    bulk.append(source_doc)
                    p_queue.task_done()

                try_counter = 1
                is_indexed = False
                while try_counter <= p_nbmax_retry and not is_indexed:
                    start_bulking = time.time()

                    try:
                        # Bulk indexation
                        if len(bulk) > 0:
                            helpers.bulk(es, bulk, raise_on_error=True)
                    except Exception as e:
                        logger_mp.error("Bulk not indexed in ES - Retry n°{0}".format(try_counter))
                        logger_mp.error(e)
                        try_counter += 1
                    else:
                        is_indexed = True
                        now = time.time()
                        elapsed_bulking = now - start_bulking
                        elapsed = now - start
                        with self.counters['nb_items_stored'].get_lock():
                            self.counters['nb_items_stored'].value += len(bulk)
                            self.counters['whole_storage_time'].value += elapsed
                            self.counters['bulk_storage_time'].value += elapsed_bulking
                            nb_items = self.counters['nb_items_stored'].value
                            if nb_items % self.counters['log_every'] == 0 and nb_items != 0:
                                logger_mp.info("Store : {0} items".format(nb_items))
                                logger_mp.debug("   -> Avg store time : {0}ms".format(1000 * self.counters['whole_storage_time'].value / nb_items))
                                logger_mp.debug("   -> Avg bulk time  : {0}ms".format(1000 * self.counters['bulk_storage_time'].value / nb_items))

                            start = time.time()

                if not is_indexed:
                    start = time.time()
                    logger_mp.error("Bulk not indexed in elasticsearch : operation aborted after %i retries", try_counter - 1)
                    with self.counters['nb_items_error'].get_lock():
                        self.counters['nb_items_error'].value += len(bulk)

            except KeyboardInterrupt:
                logger_mp.info("ESio.dequeue_and_store : User interruption of the process")
                # If indexing has been disabled, enable it again
                if p_disable_indexing:
                    self._enable_indexing_and_replicat(logger_mp, es, p_index, current_settings)
                poison_pill = True
                p_queue.task_done()
            except Exception as e:
                logger_mp.error("An error occured while storing elements to ES : {0}".format(e))
                main_loop_retry += 1
                if main_loop_retry >= main_loop_max_retry:
                    poison_pill = True
                    p_queue.task_done()

        # If indexing has been disabled, enable it again
        if p_disable_indexing:
            try:
                self._enable_indexing_and_replicat(logger_mp, es, p_index, current_settings)
            except Exception as e:
                logger_mp.error("Can't enable indexing and replicat again on {} from previous settings {}".format(p_index, current_settings))
                logger_mp.error(e)

    def scan_and_queue(self, p_queue, p_index, p_query={}, p_doctype=None, p_scroll_time='5m', p_timeout='1m', p_size=100, p_overall_timeout=30, p_nbmax_retry=3):
        """Reads docs from an es index according to a query and pushes them to the queue

            p_queue:         Queue where items are pushed to
            p_scroll_time:    Time for scroll method
            p_timeout:        Timeout - After this period, scan context is closed
            p_index:        Index where items are picked from
            p_doctype:        DocType of the items
            p_query:        ElasticSearch query for scanning the index
        """
        logger_mp = get_logger_mp(__name__, self.log_queue, self.log_level, self.formatter)

        try:
            param = [{'host': self.host, 'port': self.port, 'timeout': p_overall_timeout, 'max_retries': p_nbmax_retry, 'retry_on_timeout': True}]
            if self.proxy is None:
                es = Elasticsearch(param)
            else:
                es = Elasticsearch(param, connection_class=MyConnection, proxies={'http': self.proxy})
            es.ping()
            logger_mp.info('Connected to ES Server for reading: {0}'.format(json.dumps(param)))
        except Exception as e:
            logger_mp.error('Connection failed to ES Server for reading: {0}'.format(json.dumps(param)))
            logger_mp.error(e)

        try:
            if not self.scroll_docs:
                if 'p_doctype' is not None:
                    self.scroll_docs = helpers.scan(client=es, query=p_query, size=p_size, scroll=p_scroll_time, index=p_index, doc_type=p_doctype, timeout=p_timeout)
                else:
                    self.scroll_docs = helpers.scan(client=es, query=p_query, size=p_size, scroll=p_scroll_time, index=p_index, timeout=p_timeout)

            start = time.time()
            for doc in self.scroll_docs:
                p_queue.put(doc)

                elapsed = time.time() - start

                with self.counters['nb_items_scanned'].get_lock():
                    self.counters['nb_items_scanned'].value += 1
                    nb_items = self.counters['nb_items_scanned'].value
                    self.counters['scan_time'].value += elapsed

                    if nb_items % self.counters['log_every'] == 0:
                        logger_mp.info("Scan : {0} items".format(nb_items))
                        logger_mp.debug("   -> Avg scan time : {0}ms".format(1000 * self.counters['scan_time'].value / nb_items))

                    # Start timers reinit
                    start = time.time()

        except Exception as e:
            logger_mp.info("Error while scanning ES index %s with query %s", p_index, p_query)
            with self.counters['nb_items_error'].get_lock():
                self.counters['nb_items_error'].value += 1

    def _disable_indexing_and_replicat(self, p_logger, p_es_client, p_index):
        """
            Disable the indexing process : set the refresh rate to -1 and the number of replicat to 0
        """
        self._set_indexing_and_replicat(p_logger, p_es_client, p_index, p_refresh_rate="-1", p_num_replicat=0)

    def _enable_indexing_and_replicat(self, p_logger, p_es_client, p_index, p_default_settings={}):
        """
            Enable the indexing process by applying a default setting for refresh rate (1s) and num of replicat
        """
        refresh_rate = p_default_settings.get('index', {}).get('refresh_interval', '1s')
        num_replicat = p_default_settings.get('index', {}).get('number_of_replicas', 1)
        self._set_indexing_and_replicat(p_logger, p_es_client, p_index, p_refresh_rate=refresh_rate, p_num_replicat=num_replicat)

    def _set_indexing_and_replicat(self, p_logger, p_es_client, p_index, p_refresh_rate="1s", p_num_replicat=1):
        """
            Set the refresh rate for a given index
        """
        if p_refresh_rate == "-1":
            p_logger.warn("Indexing disabled for index {0}".format(p_index))
        else:
            p_logger.warn("Indexing enabled for index {0}".format(p_index))

        if p_num_replicat == 0:
            p_logger.warn("No replicat set for index {0}".format(p_index))
        else:
            p_logger.warn("Index {0} set with {1} replicats".format(p_index, p_num_replicat))

        # Enable indexing again
        settings = {
            "index": {
                "refresh_interval": p_refresh_rate,
                "number_of_replicas": p_num_replicat
            }
        }

        if not p_es_client.indices.exists(index=p_index):
            try:
                p_es_client.indices.create(index=p_index, body={'settings': settings})
            except Exception as e:
                p_logger.info("Can't create index {0}, already exists ?".format(p_index))
                p_logger.info(e)
        else:
            p_es_client.indices.put_settings(body=settings, index=p_index)
