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

import os
import pwd
import grp
import random
import hashlib
from corenetwork.utils import system
from corenetwork.utils import config
from corenetwork.utils.logger import log

def change_user(user, group):
    def result():
        log(msg="executing as %s:%s" % (str(user), str(group)), tags=('system', 'info'))

        if group is not None:
            os.setgid(grp.getgrnam(group).gr_gid)

        if user is not None:
            os.setuid(pwd.getpwnam(user).pw_uid)
    return result


class OsMixin():
    def _check_i_am_root(self):
        if os.getuid() != 0:
            raise Exception('not_root_user')


    def _check_i_am_cloudover(self):
        uid_cloudover = pwd.getpwnam(config.get('agent', 'WORKER_USER')).pw_uid
        if os.getuid() != uid_cloudover:
            raise Exception('not_cloudover_user')


    def _become_cloudover(self):
        """
        Change uid and git to cloudover user (or specified in settings user)
        """
        log(msg="become_cloudover: switching to user cloudover", tags=('system', 'info'))

        uid_cloudover = pwd.getpwnam('cloudover').pw_uid

        groups = []
        gid_cloudover = grp.getgrnam('cloudover').gr_gid
        groups.append(gid_cloudover)
        groups.append(grp.getgrnam('kvm').gr_gid)
        try:
            groups.append(grp.getgrnam('fuse').gr_gid)
        except:
            pass

        try:
            groups.append(grp.getgrnam('libvirt').gr_gid)
        except:
            groups.append(grp.getgrnam('libvirtd').gr_gid)


        if os.getuid() == 0:
            os.environ['HOME'] = '/var/lib/cc1/'
            os.setgroups(groups)
            os.setgid(gid_cloudover)
            os.setuid(uid_cloudover)
        elif os.getuid() != uid_cloudover:
            raise Exception("cannot_switch_to_user_cloudover")


    def _configure_core_user(self):
        '''
        Configure user's account at core
        '''
        key_dir = os.path.join(pwd.getpwnam(config.get('agent', 'WORKER_USER')).pw_dir, '.ssh')
        if not os.path.exists(key_dir):
            os.mkdir(key_dir)

        if not os.path.exists(key_dir + '/id_rsa'):
            config_file = open(os.path.join(key_dir, 'config'), 'w')
            config_file.write('Host *\n')
            config_file.write('  StrictHostKeyChecking no\n')
            config_file.write('  UserKnownHostsFile /dev/null\n')
            config_file.close()

            system.call(['ssh-keygen', '-t', 'rsa', '-N', '', '-f', os.path.join(key_dir, 'id_rsa')])
            os.chown(key_dir, pwd.getpwnam(config.get('agent', 'WORKER_USER')).pw_uid, pwd.getpwnam(config.get('agent', 'WORKER_USER')).pw_gid)
            os.chown(key_dir + '/config', pwd.getpwnam(config.get('agent', 'WORKER_USER')).pw_uid, pwd.getpwnam(config.get('agent', 'WORKER_USER')).pw_gid)
            os.chown(key_dir + '/id_rsa', pwd.getpwnam(config.get('agent', 'WORKER_USER')).pw_uid, pwd.getpwnam(config.get('agent', 'WORKER_USER')).pw_gid)

            os.chmod(key_dir, 0700)
            os.chmod(key_dir + '/id_rsa', 0700)


    def _configure_node_user(self):
        '''
        Setup user's account at node
        '''
        log(msg="setup_user: configuring user account", tags=('system', 'info'))
        auth_seed = hashlib.sha256(str(random.random())).hexdigest()
        try:
            key_info = self._request('ci/node/get_authorized_keys/', {'auth_hash': self._calc_hash(config.get('node', 'AUTH_TOKEN'), auth_seed),
                                                                      'auth_seed': auth_seed})
            key_dir = os.path.join(pwd.getpwnam(key_info['user']).pw_dir, '.ssh')
            key_path = os.path.join(key_dir, 'authorized_keys')
            if not os.path.exists(key_dir):
                os.mkdir(key_dir, 0700)
            key_file = open(key_path, 'w')
            key_file.write(key_info['keys'])
            key_file.close()
            os.chmod(key_path, 0600)
            os.chown(key_dir, pwd.getpwnam(key_info['user']).pw_uid, pwd.getpwnam(key_info['user']).pw_gid)
            os.chown(key_path, pwd.getpwnam(key_info['user']).pw_uid, pwd.getpwnam(key_info['user']).pw_gid)
        except Exception as e:
            print str(e)
            self._request('ci/node/update_state/', {'auth_hash': self._calc_hash(config.get('node', 'AUTH_TOKEN'), auth_seed),
                                                    'auth_seed': auth_seed,
                                                    'state': 'lock',
                                                    'comment': 'Cannot update ssh key: %s' % str(e)})
