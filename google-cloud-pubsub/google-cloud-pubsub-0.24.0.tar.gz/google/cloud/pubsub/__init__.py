# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Pubsub API wrapper.

The main concepts with this API are:

- :class:`~google.cloud.pubsub.topic.Topic` represents an endpoint to which
  messages can be published using the Cloud Storage Pubsub API.

- :class:`~google.cloud.pubsub.subscription.Subscription` represents a named
  subscription (either pull or push) to a topic.
"""


from pkg_resources import get_distribution
__version__ = get_distribution('google-cloud-pubsub').version

from google.cloud.pubsub.client import Client
from google.cloud.pubsub.subscription import Subscription
from google.cloud.pubsub.topic import Topic

__all__ = ['__version__', 'Client', 'Subscription', 'Topic']
