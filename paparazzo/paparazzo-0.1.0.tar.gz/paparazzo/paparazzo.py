#!/bin/python2
from elasticsearch import Elasticsearch
from .exceptions import PaparazzoError
import logging


class Paparazzo:

    def __init__(self, hosts, access_key, secret_key, region, bucket, **kwargs):
        self.hosts = hosts
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.bucket = bucket
        self.logger = logging.getLogger(__name__)

        log_handler = kwargs.get('log_handler', None)
        if log_handler:
            self.logger.addHandler(log_handler)

    def snapshot_from_indices(self, indices, repository_name, snapshot_name):
        """
        Take a snapshot of the given indices and store them in the S3 bucket specified during initialisation
        
        :param indices: The indices to snapshot
        :param repository_name: The Elasticsearch repository name
        :param snapshot_name: The snapshot name
        :return: bool
        :raise: PaparazzoError
        """

        # Connect to the Elasticsearch host(s)
        es = self.__connect_to_elasticsearch()

        # Create a repository using the Elasticsearch instance
        self.__create_repository(es, repository_name)

        self.logger.info('Snapshotting indices')

        try:
            es.snapshot.create(
                repository=repository_name,
                snapshot=snapshot_name,
                body={
                    'indices': indices
                },
                wait_for_completion=True
            )

            self.logger.info('Snapshot complete')
        except Exception, e:
            self.logger.error('An error occurred during snapshot creation')
            self.logger.error('Error: ' + str(e))
            raise PaparazzoError('Snapshot creation failed: ' + str(e))

        return True

    def restore_from_snapshot(self, indices, repository_name, snapshot_name):
        """
        Restore data from a snapshot
        
        :param indices: The indices to restore data to
        :param repository_name: The Elasticsearch repository name
        :param snapshot_name: The snapshot name
        :return: bool
        :raise: PaparazzoError
        """

        # Connect to the Elasticsearch host(s)
        es = self.__connect_to_elasticsearch()

        # Create a repository using the Elasticsearch instance
        self.__create_repository(es, repository_name)

        self.logger.info('Closing indices before restoring data')

        # Must close indices before restoring
        for index in indices:

            self.logger.info('Closing index: ' + index)

            try:
                es.indices.close(index=index, ignore_unavailable=True)
            except Exception, e:
                self.logger.error('An error occurred whilst trying to close index: ' + index)
                self.logger.error('Error: ' + str(e))
                self.__force_open_indices(es, indices)
                raise PaparazzoError('Elasticsearch indices could not be closed: ' + str(e))

        self.logger.info('Restoring indices from S3 snapshot')

        try:
            es.snapshot.restore(
                repository=repository_name,
                snapshot=snapshot_name,
                body={
                    'indices': indices
                },
                wait_for_completion=False
            )
        except Exception, e:
            self.logger.error('An error occurred whilst trying to perform snapshot restoration')
            self.logger.error('Error: ' + str(e))
            raise PaparazzoError('Snapshot restoration could not be completed: ' + str(e))
        finally:
            self.__force_open_indices(es, indices)

        return True

    def __connect_to_elasticsearch(self):
        """
        Connect to the Elasticsearch hosts and return the Elasticsearch instance

        :return: Elasticsearch
        :raise: PaparazzoError
        """

        self.logger.info('Attempting to connect to Elasticsearch cluster')

        try:
            es = Elasticsearch(
                self.hosts,
                sniff_on_start=True,
                sniff_on_connection_fail=True,
                sniffer_timeout=60
            )

            self.logger.info('Connected to Elasticsearch!')
            return es
        except Exception, e:
            self.logger.error('An error occurred whilst trying to connect to Elasticsearch')
            self.logger.error('Error: ' + str(e))
            raise PaparazzoError('Connection to Elasticsearch could not be established: ' + str(e))

    def __create_repository(self, es, repository_name):
        """
        Create a repository using given Elasticsearch instance

        :param es: Elasticsearch 
        :param repository_name: The repository name to create
        :return: bool
        :raise: PaparazzoError
        """

        self.logger.info('Creating repository')

        try:
            es.snapshot.create_repository(
                repository=repository_name,
                body={
                    'type': 's3',
                    'settings': {
                        'region': self.region,
                        'bucket': self.bucket,
                        'access_key': self.access_key,
                        'secret_key': self.secret_key
                    }
                },
                request_timeout=30,
                verify=False
            )
        except Exception, e:
            self.logger.error('An error occurred during the repository creation')
            self.logger.error('Error: ' + str(e))
            raise PaparazzoError('The repository could not be created: ' + str(e))

        self.logger.info('Created repository!')
        return True

    def __force_open_indices(self, es, indices):
        """
        Open Elasticsearch indices
        (Usually performed after the snapshot process)
        
        :param es: Elasticsearch
        :param indices: List of indices to open
        :return: bool
        :raise: PaparazzoError
        """

        self.logger.info('Opening indices')

        try:
            for index in indices:
                self.logger.info('Opening index: ' + index)
                es.indices.open(index=index, ignore_unavailable=True)
        except Exception, e:
            self.logger.error('An error occurred during the opening of the indices')
            self.logger.error('Error: ' + str(e))
            raise PaparazzoError('The Elasticsearch indices could not be opened: ' + str(e))

        return True
