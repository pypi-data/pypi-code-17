# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy

from altuscli import exceptions
from altuscli.extensions.dataeng import dataengutils

import mock

from tests import unittest

from . import SAMPLE_DESCRIBE_CLUSTERS


class TestDataEngUtils(unittest.TestCase):

    def setUp(self):
        self.clusters = SAMPLE_DESCRIBE_CLUSTERS

    @mock.patch('altuscli.extensions.dataeng.dataengutils.get_client')
    def test_get_clusters(self, get_client_mock):
        client = mock.Mock()
        get_client_mock.return_value = client

        dataengutils.get_clusters(None, None, 'cluster-name')

        self.assertTrue(client.describe_clusters.called)
        client.describe_clusters.assert_called_with(
            clusterNames=['cluster-name'])

    def test_get_single_cluster(self):
        self.assertEqual(dataengutils.get_single_cluster(self.clusters,
                                                         'cluster-name'),
                         self.clusters["clusters"][0])

    def test_get_single_cluster_with_invalid_format(self):
        local_clusters = copy.deepcopy(self.clusters)
        local_clusters['clusters'].append([])

        with self.assertRaises(exceptions.MultipleClustersExist):
            dataengutils.get_single_cluster(local_clusters, 'cluster-name')

    def test_get_cm_endpoint(self):
        self.assertEqual(dataengutils.get_cm_endpoint(self.clusters["clusters"][0],
                                                      'cluster-name'),
                         self.clusters["clusters"][0]["clouderaManagerEndpoint"])

    def test_get_terminating_cluster_cm_endpoint(self):
        local_clusters = copy.deepcopy(self.clusters)
        local_clusters['clusters'][0]['status'] = 'TERMINATING'

        cluster = dataengutils.get_single_cluster(local_clusters,
                                                  'cluster-name')

        with self.assertRaises(exceptions.ClusterTerminatingError):
            dataengutils.get_cm_endpoint(cluster,
                                         'cluster-name')
