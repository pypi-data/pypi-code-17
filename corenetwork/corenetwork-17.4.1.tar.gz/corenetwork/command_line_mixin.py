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

import hashlib
import libvirt
import random
import re
import sys
import time

from datetime import datetime, timedelta
from django.db.models import Q
from corenetwork.hook_interface import HookInterface
from corenetwork.utils import config


class CommandLineMixin():
    def info_node(self, action, id=None):
        from corecluster.models.core.node import Node
        from corecluster.cache.task import Task
        if action == 'list':
            print "ID\t\t\t\t\tAddress\t\tState\tRunning VMs"
            for node in Node.objects.all():
                print "%s\t%s\t%s\t%d" % (node.id, node.address, node.state, len(node.vm_set.exclude(state='closed')))

        elif action == 'disable':
            node = Node.objects.get(pk=id)
            print "Disabling node %s" % node.address
            node.stop()
            node.set_state('lock')
            node.save()

        elif action == 'enable':
            node = Node.objects.get(pk=id)
            print "Enabling node %s" % node.address
            node.start()

        elif action == 'suspend':
            node = Node.objects.get(pk=id)

            print "Canceling all not active tasks for node %s" % node.id
            for task in Task.get_related(node, ['not active']):
                task.set_state('canceled')
                task.save()

            print "Suspending node %s" % node.address
            task = Task()
            task.type = 'node'
            task.action = 'suspend'
            task.append_to([node])

        elif action == 'wakeup':
            node = Node.objects.get(pk=id)
            print "Waking up node %s" % node.address
            task = Task()
            task.type = 'node'
            task.action = 'wake_up'
            task.append_to([node])

        else:
            print "node [list]"
            print "node [enable|disable|suspend|wakeup] [id]"


    def info_vm(self, action, id=None):
        from corecluster.models.core.vm import VM
        from corecluster.cache.task import Task
        if action == 'list':
            print "ID\t\t\t\t\tUser\t\t\t\t\tNode\tState"
            for vm in VM.objects.all():
                print "%s\t%s\t%s\t%s" % (vm.id, vm.user.id, vm.node.address, vm.state)

        elif action == 'erase':
            vm = VM.objects.get(pk=id)
            print "Erasing VM %s" % vm.id
            #for task in vm.task_set.exclude(state__in=['ok', 'canceled']).all():
            #    task.set_state('canceled')
            #    task.save()
            vm.cleanup(True)

        elif action == 'save':
            vm = VM.objects.get(pk=id)
            if vm.base_image is None:
                print "VM %s has no base image" % vm.id
            else:
                print "Saving VM's base image"
                task = Task()
                task.action = 'save_image'
                task.type = 'node'
                task.append_to([vm, vm.base_image, vm.node])

        elif action == 'cleanup':
            for vm in VM.objects.filter(state='closed').all():
                vm.delete()

        elif action == 'check':
            self._become_cloudover()
            vm = VM.objects.get(pk=id)
            conn = vm.node.libvirt_conn()
            domain = conn.lookupByName(vm.libvirt_name)
            print "Domain state: %d" % domain.state()[0]
            if domain.state()[0] == libvirt.VIR_DOMAIN_RUNNING:
                vm.set_state('running')
                vm.save()
            else:
                vm.set_state('stopped')
                vm.save()

        elif action == 'vnc':
            vm = VM.objects.get(pk=id)
            print str(vm.node.address) + ':' + str(vm.vnc_port)

        elif action == 'websocket':
            vm = VM.objects.get(pk=id)
            lease = vm.lease_set.filter(mode='routed').first()
            if lease == None:
                print ''
            else:
                print str(lease.vm_address) + ':' + str(vm.websocket_port)

        elif action == 'webvnc':
            vm = VM.objects.get(pk=id)
            if vm.vnc_enabled:
                sys.stdout.write('http://' + str(vm.node.address) + ':1' + str(vm.vnc_port))
            else:
                sys.exit(1)

        else:
            print "vm [list|cleanup]"
            print "vm [erase|check|save] [id]"


    def _print_blockers(self, task, indent=0):
        for blocker in task.blockers.all():
            print "  %s%s:%s:\t\t%s\t%s" % (' ' * indent, blocker.type, blocker.action, blocker.state, blocker.id)
            self._print_blockers(blocker, indent+2)


    def info_task(self, action, id=None):
        from corecluster.cache.task import Task
        from corecluster.cache import Cache

        if action == 'list':
            print('ID\t\t\t\t\tType\t\tAction\t\tState')
            tasks = [Task(data=t) for t in Cache.hvals(Task.container)]
            for task in tasks:
                print '%s\t%s\t\t%s\t\t%s' % (task.id, task.type, task.action, task.state)

        elif action == 'list-active':
            print('ID\t\t\t\t\tType\t\tAction\t\tState')
            tasks = [Task(data=t) for t in Cache.hvals(Task.container)]
            for task in tasks:
                if task.state not in ['ok', 'canceled']:
                    print '%s\t%s\t\t%s\t\t%s' % (task.id, task.type, task.action, task.state)

        elif action == 'blockers' and id is not None:
            print('Not supported')

        elif action == 'delete' and id is not None:
            tasks = [Task(data=t) for t in Cache.hvals(Task.container)]
            if id == 'all':
                for k in Cache.keys():
                    print('Deleting %s' % k)
                    Cache.delete(k)
            elif id == 'failed':
                for task in tasks:
                    if task.state == 'failed':
                        print('Deleting task %s' % task)
                        task.delete()
            elif id == 'done':
                for task in tasks:
                    if task.state in ['ok', 'canceled']:
                        task.delete()
            else:
                for task_id in Cache.hkeys(Task.container):
                    if task_id.endswith(':' + id):
                        task = Task(cache_key=task_id)
                        task.delete()
                        return

        elif action == 'cleanup':
            tasks = [Task(data=t) for t in Cache.hvals(Task.container)]
            for task in tasks:
                if task.state in ['ok', 'canceled']:
                    task.delete()

        elif action == 'cancel' and id is not None:
            tasks = [Task(data=t) for t in Cache.hvals(Task.container)]
            if id == 'all':
                for task in tasks:
                    print "Deleting %s" % task.id
                    task.set_state('canceled')
                    task.save()
            else:
                for task_id in Cache.hkeys(Task.container):
                    if task_id.endswith(':' + id):
                        task = Task(cache_key=task_id)
                        print "Canceling %s" % task.id
                        task.set_state('canceled')
                        task.save()
                        return

        elif action == 'info' and id is not None:
            for task_id in Cache.hkeys(Task.container):
                if task_id.endswith(':' + id):
                    task = Task(cache_key=task_id)

                    print("ID: " + task.id)
                    print("State: " + str(task.state))
                    print("Blocked by: " + ', '.join(Cache.lrange('blockers:' + task.cache_key(), 0, Cache.llen('blockers:' + task.cache_key()))))
                    print("Type: " + str(task.type) + "-" + str(task.action))
                    print("Comments: " + str(task.comment))
                    print("Data: " + str(task.data))
                    if task.agent_id is not None:
                        print "Agent: " + str(task.agent_id)
                    else:
                        print "Agent: None"

        elif action == 'dump' and id is not None:
            for task_id in Cache.hkeys(Task.container):
                if task_id.endswith(':' + id):
                    print Cache.hget(Task.container, task_id)

        elif action == 'restart' and id is not None:
            tasks = [Task(data=t) for t in Cache.hvals(Task.container)]
            if id == 'all':
                for task in tasks:
                    print "Restarting %s" % task.id
                    task.set_state('not active')
                    task.agent = None
                    task.save()
            else:
                for task_id in Cache.hkeys(Task.container):
                    if task_id.endswith(':' + id):
                        task = Task(cache_key=task_id)
                        task.set_state('not active')
                        task.agent = None
                        task.save()
                        return

        else:
            print("task [list|info-active]")
            print("task [blockers|delete|cancel|dump|restart|info] [id|all]")
            print("     task delete all removes all cache contents, including locks")


    def info_agent(self, action, id=None):
        from corecluster.models.core.agent import Agent
        if action == 'list':
            print "ID\t\t\t\t\tType\t\tPID\tHostname\t\tState"
            for agent in Agent.objects.all():
                print "%s\t%s\t\t%d\t%s\t%s" % (agent.id, agent.type, agent.pid, agent.hostname, agent.state)

        elif action == 'shutdown' and id != None:
            if id == 'all':
                for agent in Agent.objects.filter(state='running'):
                    print "Shutting down agent %s:%d (ID:%s)" % (agent.type, agent.pid, agent.id)
                    agent.set_state('stopping')
                    agent.save()
            else:
                agent = Agent.objects.get(pk=id)
                print "Shutting down agent %s:%d (ID:%s)" % (agent.type, agent.pid, agent.id)
                agent.set_state('stopping')
                agent.save()

        elif action == 'check':
            for agent in Agent.objects.filter(alive__lt=datetime.now()-timedelta(hours=2)):
                agent.set_state('done')
                agent.save()

        elif action == 'cleanup':
            for agent in Agent.objects.filter(state__in=['stopping', 'done']):
                agent.delete()

        else:
            print "agent [list|check|cleanup]"
            print "shutdown [shutdown] [id|all]"


    def info_subnet(self, action, id=None):
        from corecluster.models.core.subnet import Subnet

        if action == 'list':
            print "ID\t\t\t\t\tUser\t\t\t\t\tAddress\t\tMode\tPool"
            for un in Subnet.objects.all():
                print "%s\t%s\t%s/%d\t%s\t%s/%d" % (un.id, un.user.id, un.address, un.mask, un.network_pool.mode, un.network_pool.address, un.network_pool.mask)

        elif action == 'delete':
            un = Subnet.objects.get(pk=id)
            if not un.is_in_use():
                print "Scheduling network %s delete" % un.id
                un.release()
            else:
                print "Network is in use"

        elif action == 'lease_list':
            un = Subnet.objects.get(pk=id)
            print "ID\t\t\t\t\tVM Address\tVM"
            for lease in un.lease_set.all():
                print "%s\t%s\t%s" % (lease.id, lease.vm_address, str(lease.vm))
        else:
            print "subnet [list]"
            print "subnet [lease_list|delete] [id]"


    def info_network_pool(self, action, id=None):
        from corecluster.models.core.network_pool import NetworkPool
        if action == 'list':
            print "ID\t\t\t\t\tMode\tAddress\tSubnets"
            for np in NetworkPool.objects.all():
                print "%s\t%s\t%s/%d\t%d" % (np.id, np.mode, np.address, np.mask, np.subnet_set.count())

        elif action == 'subnet_list':
            np = NetworkPool.objects.get(pk=id)
            print "ID\t\t\t\t\tAddress"
            for sn in np.subnet_set.all():
                print "%s\t%s/%d" % (sn.id, sn.address, sn.mask)
        else:
            print "network_pool [list]"
            print "network_pool [subnet_list] [id]"


    def info_storage(self, action, id=None):
        from corecluster.models.core.storage import Storage
        from corecluster.cache.task import Task
        from corecluster.models.core.node import Node

        if action == 'list':
            print "ID\t\t\t\t\tState\tTransport\tAddress\t\tDir\tName\tImages"
            for s in Storage.objects.all():
                print "%s\t%s\t%s\t\t%s\t%s\t%s\t%d" % (s.id, s.state, s.transport, s.address, s.dir, s.name, len(s.image_set.filter(state='ok').all()))

        elif action == 'lock':
            s = Storage.objects.get(pk=id)
            s.set_state('locked')
            s.save()

            mnt = Task()
            mnt.type = 'storage'
            mnt.action = 'umount'
            mnt.append_to([s])

            for node in Node.objects.filter(state='ok'):
                umount_ok = True
                for vm in node.vm_set.all():
                    for image in vm.image_set.all():
                        if image.storage == s:
                            print("WARNING: VM %s at node %s uses selected storage!" % (vm.id, node.address))
                            umount_ok = False

                if umount_ok:
                    mnt = Task()
                    mnt.type = 'node'
                    mnt.action = 'umount'
                    mnt.append_to([s, node])

        elif action == 'unlock':
            s = Storage.objects.get(pk=id)
            s.set_state('locked')
            s.save()

            mnt = Task()
            mnt.type = 'storage'
            mnt.action = 'mount'
            mnt.state = 'not active'
            mnt.append_to([s])

            for node in Node.objects.filter(state='ok'):
                node.set_state('offline')
                node.save()

            for node in Node.objects.filter(Q(state='ok') | Q(state='offline')):
                node.start()
        else:
            print "storage [list]"
            print "storage [lock|unlock] [id]"


    def info_api(self, action, id=None):
        from corecluster.models.core.permission import Permission
        if action == 'list':
            print "Function\tCalls\tAverage time"
            for p in Permission.objects.all():
                print "%s\t%s\t%s" % (p.function, p.requests, p.average_time)
        else:
            print("api [list]")


    def info_image(self, action, id=None):
        from corecluster.models.core.image import Image
        from corecluster.cache.task import Task

        if action == 'list':
            print "ID\t\t\t\t\tState\tStorage\tName"
            for image in Image.objects.exclude(state='deleted'):
                print "%s\t%s\t%s\t%s" % (image.id, image.state, image.storage.name, image.name)
        elif action == 'delete' and id is not None:
            image = Image.objects.get(pk=id)
            t = Task()
            t.type = 'image'
            t.action = 'delete'
            t.ignore_errors = True
            t.append_to([image, image.storage])
        else:
            print("image [list]")
            print("image [delete] [id]")


    def info_cron(self, action, id=None):
        self._become_cloudover()
        hooks = []
        if action == 'minute':
            hooks = HookInterface.get_hooks('cron.minute')
        elif action == 'hourly':
            hooks = HookInterface.get_hooks('cron.hourly')
        elif action == 'daily':
            hooks = HookInterface.get_hooks('cron.daily')
        elif action == 'weekly':
            hooks = HookInterface.get_hooks('cron.weekly')
        elif action == 'monthly':
            hooks = HookInterface.get_hooks('cron.monthly')
        else:
            print("cron [minute|hourly|daily|weekly|monthly]")

        for hook in hooks:
            if hasattr(hook, 'cron'):
                hook.cron()


    def info_cloudinit(self, vm_address):
        core_ip = self._get_core_address()
        auth_seed = hashlib.sha256(str(random.random())).hexdigest()
        auth_hash = self._calc_hash(config.get('node', 'AUTH_TOKEN'), auth_seed)
        sys.stdout.write("http://%s:8600/%s/%s/%s/" % (core_ip, auth_hash, auth_seed, vm_address))


    def info_log(self, action, id=None):
        from corenetwork.models.message import Message
        from corenetwork.models.tag import Tag


        if id is not None:
            tags = Tag.objects.filter(name__in=id.split(',')).all()
            if len(tags) == 0:
                print('Tag not found')
                return

            q = tags[0].message_set.all()
            for tag in tags[1:]:
                q = q & tag.message_set.all()
        else:
            q = Message.objects

        if action == 'help':
            print("log [all|clear|PERIOD] [tag1,tag2,...]")
            print("    Prints logs with last N minutes(m), hours (H), days(D), weeks(W), months(M), or all(all)")
            print("    for example cc-manage 3D agent,vm will show messages from last three days.")
            print("    Use clear to remove all messages from logs database")
            print("    Optionally you can specify required tags as additional parameter.")
            return

        elif action == 'clear':
            Message.objects.all().delete()
            print('Deleted all logs')
            return

        elif action == 'watch':
            last_id = None
            while True:
                if id is not None:
                    tags = Tag.objects.filter(name__in=id.split(',')).all()
                    if len(tags) == 0:
                        print('Tag not found')
                        return

                    q = tags[0].message_set.all()
                    for tag in tags[1:]:
                        q = q & tag.message_set.all()
                else:
                    q = Message.objects

                q.order_by('date')

                if last_id is not None:
                    result = q.filter(id__gt=last_id).all()
                    for msg in result:
                        print(str(msg))
                        last_id = msg.id
                else:
                    last_id = q.last().id
                time.sleep(0.5)

        elif action != 'all':
            digits = int(re.findall('\d+', action)[0])
            if action[-1] in ['m', 'min', 'minute', 'minutes']:
                q = q.filter(date__range=(datetime.now() - timedelta(minutes=digits), datetime.now()))
            elif action[-1] in ['h', 'H', 'hour', 'hours']:
                q = q.filter(date__range=(datetime.now() - timedelta(hours=digits), datetime.now()))
            elif action[-1] in ['d', 'D', 'day', 'days']:
                q = q.filter(date__range=(datetime.now() - timedelta(days=digits), datetime.now()))
            elif action[-1] in ['w', 'W', 'week', 'weeks']:
                q = q.filter(date__range=(datetime.now() - timedelta(weeks=digits), datetime.now()))

        for msg in q.order_by('date').all():
            print(str(msg))
