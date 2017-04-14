"""
Copyright (C) 2014-2017 cloudover.io ltd.
This file is part of the CloudOver.org project

Licensee holding a valid commercial license for this software may
use it in accordance with the terms of the license agreement
between cloudover.io ltd. and the licensee.
 
Alternatively you may use this software under following terms of
GNU Affero GPL v3 license:

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version. For details contact
with the cloudover.io company: https://cloudover.io/


This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.


You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from django.conf.urls import url

urlpatterns = [
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/$', 'coretalk.views.cloudinit.functions.get_root'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/latest/?$', 'coretalk.views.cloudinit.functions.get_latest'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/latest/meta-data/?$', 'coretalk.views.cloudinit.functions.get_meta_data'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/latest/meta-data/ami-id$', 'coretalk.views.cloudinit.functions.get_ami_id'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/latest/meta-data/hostname$', 'coretalk.views.cloudinit.functions.get_hostname'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/latest/meta-data/instance-id$', 'coretalk.views.cloudinit.functions.get_instance_id'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/latest/meta-data/instance-type$', 'coretalk.views.cloudinit.functions.get_instance_type'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/latest/meta-data/public-keys/?$', 'coretalk.views.cloudinit.functions.get_public_keys'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/latest/meta-data/public-keys/(?P<id>[a-zA-Z0-9\-]+)/?$', 'coretalk.views.cloudinit.functions.get_public_key_formats'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/latest/meta-data/public-keys/(?P<id>[a-zA-Z0-9\-]+)/openssh-key$', 'coretalk.views.cloudinit.functions.get_public_key'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/latest/user-data/?$', 'coretalk.views.cloudinit.functions.get_user_data'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/\d{2,4}-\d{1,2}-\d{1,2}/?$', 'coretalk.views.cloudinit.functions.get_latest'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/\d{2,4}-\d{1,2}-\d{1,2}/meta-data/?$', 'coretalk.views.cloudinit.functions.get_meta_data'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/\d{2,4}-\d{1,2}-\d{1,2}/meta-data/ami-id$', 'coretalk.views.cloudinit.functions.get_ami_id'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/\d{2,4}-\d{1,2}-\d{1,2}/meta-data/hostname$', 'coretalk.views.cloudinit.functions.get_hostname'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/\d{2,4}-\d{1,2}-\d{1,2}/meta-data/instance-id$', 'coretalk.views.cloudinit.functions.get_instance_id'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/\d{2,4}-\d{1,2}-\d{1,2}/meta-data/instance-type$', 'coretalk.views.cloudinit.functions.get_instance_type'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/\d{2,4}-\d{1,2}-\d{1,2}/meta-data/public-keys/?$', 'coretalk.views.cloudinit.functions.get_public_keys'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/\d{2,4}-\d{1,2}-\d{1,2}/meta-data/public-keys/(?P<id>[a-zA-Z0-9\-]+)/?$', 'coretalk.views.cloudinit.functions.get_public_key_formats'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/\d{2,4}-\d{1,2}-\d{1,2}/meta-data/public-keys/(?P<id>[a-zA-Z0-9\-]+)/openssh-key$', 'coretalk.views.cloudinit.functions.get_public_key'),
    url(r'^/?(?P<auth_hash>[a-zA-Z0-9]+)/(?P<auth_seed>[a-zA-Z0-9]+)/(?P<vm_ip>[0-9\.]+)/\d{2,4}-\d{1,2}-\d{1,2}/user-data/?$', 'coretalk.views.cloudinit.functions.get_user_data'),
]

