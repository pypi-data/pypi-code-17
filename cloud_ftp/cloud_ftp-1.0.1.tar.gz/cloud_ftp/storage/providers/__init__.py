# Copyright 2017 Real Kinetic, LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

"""
Provides interfaces into the possible storage systems used.  Any storage system,
including home grown generic HTTP interfaces, can be used to store the file,
except FTP itself.  It must exist on one of Google's approved ports.  GCS is
simply a very simple mechanism to do this and this provider is provided by
default.
"""
