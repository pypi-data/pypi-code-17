#
# QEMU testbed for Rumba
#
#    Vincenzo Maffione  <v.maffione@nextworks.it>
#    Marco Capitani <m.capitani@nextworks.it>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301  USA
import multiprocessing
import time
import subprocess
import os

import rumba.model as mod
import rumba.log as log
import rumba.ssh_support as ssh_support


logger = log.get_logger(__name__)


class Testbed(mod.Testbed):
    def __init__(self, exp_name, bzimage, initramfs, proj_name="ARCFIRE",
                 password="root", username="root",
                 use_vhost=True, qemu_logs_dir=None):
        mod.Testbed.__init__(self, exp_name, username, password, proj_name)
        self.vms = {}
        self.shims = []
        self.bzimage = bzimage
        self.initramfs = initramfs
        self.vhost = use_vhost
        self.qemu_logs_dir = os.getcwd() if qemu_logs_dir is None \
            else qemu_logs_dir
        self.boot_processes = []

    @staticmethod
    def _run_command_chain(commands, results_queue,
                           error_queue, ignore_errors=False):
        """
        Runs (sequentially) the command list.

        On error, breaks and dumps it in error_queue, and interrupts
        as soon as it is non-empty (unless ignore errors is True).

        :type commands: list
        :type results_queue: Queue
        :type error_queue: Queue
        :param commands: list of commands to execute
        :param results_queue: Queue of results of parallel processes
        :param error_queue: Queue of error(s) encountered
        :return: None
        """
        errors = 0
        for command in commands:
            if not error_queue.empty() and not ignore_errors:
                break
            logger.debug('executing >> %s', command)
            try:
                subprocess.check_call(command.split())
            except subprocess.CalledProcessError as e:
                error_queue.put(str(e))
                errors += 1
                if not ignore_errors:
                    break
        if errors == 0:
            results_queue.put("Command chain ran correctly")
        else:
            results_queue.put("Command chain ran with %d errors" % errors)

    def recover_if_names(self, experiment):
        for node in experiment.nodes:
            for ipcp in node.ipcps:
                if isinstance(ipcp, mod.ShimEthIPCP):
                    shim_name, node_name = ipcp.name.split('.')
                    port_set = [x for x in self.vms[node_name]['ports']
                                if x['shim'].name == shim_name]
                    port = port_set[0]
                    port_id = port['port_id']
                    vm_id = self.vms[node_name]['id']
                    mac = '00:0a:0a:0a:%02x:%02x' % (vm_id, port_id)
                    logger.info('Recovering ifname for port: %s.',
                                port['tap_id'])
                    output = ssh_support.execute_command(
                        self,
                        node.ssh_config,
                        'mac2ifname ' + mac)
                    ipcp.ifname = output
                    ssh_support.execute_command(
                        self, node.ssh_config,
                        "ip link set %(ifname)s up"
                        % {'ifname': ipcp.ifname})

    def swap_in(self, experiment):
        """
        :type experiment mod.Experiment
        :param experiment: The experiment running
        """
        if os.geteuid() != 0:
            try:
                subprocess.check_call(["sudo", "-v"])
            except subprocess.CalledProcessError:
                raise Exception('Not authenticated')

        logger.info("swapping in")
        logger.info('Setting up interfaces.')

        # Building bridges and taps
        shim_processes = []
        r_queue = multiprocessing.Queue()
        e_queue = multiprocessing.Queue()
        for shim in experiment.dif_ordering:
            if not isinstance(shim, mod.ShimEthDIF):
                # Nothing to do here
                continue
            self.shims.append(shim)
            ipcps = shim.ipcps
            command_list = []
            command_list += ('sudo brctl addbr %(br)s\n'
                             'sudo ip link set %(br)s up'
                             % {'br': shim.name}
                             ).split('\n')
            for node in shim.members:  # type:mod.Node
                name = node.name
                vm = self.vms.setdefault(name, {'vm': node, 'ports': []})
                port_id = len(vm['ports']) + 1
                tap_id = '%s.%02x' % (name, port_id)

                command_list += ('sudo ip tuntap add mode tap name %(tap)s\n'
                                 'sudo ip link set %(tap)s up\n'
                                 'sudo brctl addif %(br)s %(tap)s'
                                 % {'tap': tap_id, 'br': shim.name}
                                 ).split('\n')

                if shim.link_speed > 0:
                    speed = '%dmbit' % shim.link_speed

                    # Rate limit the traffic transmitted on the TAP interface
                    command_list += (
                        'sudo tc qdisc add dev %(tap)s handle 1: root '
                        'htb default 11\n'
                        'sudo tc class add dev %(tap)s parent 1: classid '
                        '1:1 htb rate 10gbit\n'
                        'sudo tc class add dev %(tap)s parent 1:1 classid '
                        '1:11 htb rate %(speed)s'
                        % {'tap': tap_id, 'speed': speed}
                    ).split('\n')

                vm['ports'].append({'tap_id': tap_id,
                                    'shim': shim,
                                    'port_id': port_id})
                ipcp_set = [x for x in ipcps if x in node.ipcps]
                if len(ipcp_set) > 1:
                    raise Exception("Error: more than one ipcp in common "
                                    "between shim dif %s and node %s"
                                    % (shim.name, node.name))
                ipcp = ipcp_set[0]  # type: mod.ShimEthIPCP
                assert ipcp.name == '%s.%s' % (shim.name, node.name), \
                    'Incorrect Shim Ipcp found: expected %s.%s, found %s' \
                    % (shim.name, node.name, ipcp.name)
                ipcp.ifname = tap_id
                # TODO deal with Ip address (shim UDP DIF).

            # Avoid stacking processes if one failed before.
            if not e_queue.empty():
                break
            # Launch commands asynchronously
            process = multiprocessing.Process(target=self._run_command_chain,
                                              args=(command_list,
                                                    r_queue,
                                                    e_queue))
            shim_processes.append(process)
            process.start()

        # Wait for all processes to be over.
        total_processes = len(shim_processes)
        max_waiting_time = 2 * total_processes
        over_processes = 0

        while max_waiting_time > 0 and over_processes < total_processes:
            # Check for errors
            if not e_queue.empty():
                error_str = str(e_queue.get())
                logger.error('Testbed instantiation failed: %s', error_str)
                raise Exception('Failure: %s' % error_str)
            try:
                # Check for results
                result = r_queue.get(timeout=1)
                if result == "Command chain ran correctly":
                    over_processes += 1
                    logger.debug('%s/%s processes completed',
                                 over_processes, total_processes)
            except:
                max_waiting_time -= 1

        logger.info('Interfaces setup complete. '
                    'Building VMs (this might take a while).')

        # Building vms

        boot_batch_size = max(1, multiprocessing.cpu_count() // 2)
        booting_budget = boot_batch_size
        boot_backoff = 12  # in seconds
        base_port = 2222
        vm_memory = 164  # in megabytes
        vm_frontend = 'virtio-net-pci'

        vmid = 1

        for node in experiment.nodes:
            name = node.name
            vm = self.vms.setdefault(name, {'vm': node, 'ports': []})
            vm['id'] = vmid
            fwdp = base_port + vmid
            fwdc = fwdp + 10000
            mac = '00:0a:0a:0a:%02x:%02x' % (vmid, 99)
            vm['ssh'] = fwdp
            vm['id'] = vmid
            node.ssh_config.hostname = "localhost"
            node.ssh_config.port = fwdp

            vars_dict = {'fwdp': fwdp, 'id': vmid, 'mac': mac,
                         'bzimage': self.bzimage,
                         'initramfs': self.initramfs,
                         'fwdc': fwdc,
                         'memory': vm_memory, 'frontend': vm_frontend,
                         'vmname': name}

            host_fwd_str = 'hostfwd=tcp::%(fwdp)s-:22' % vars_dict
            vars_dict['hostfwdstr'] = host_fwd_str

            command = 'qemu-system-x86_64 '
            # TODO manage non default images
            command += ('-kernel %(bzimage)s '
                        '-append "console=ttyS0" '
                        '-initrd %(initramfs)s '
                        % vars_dict)
            command += ('-vga std '
                        '-display none '
                        '--enable-kvm '
                        '-smp 1 '
                        '-m %(memory)sM '
                        '-device %(frontend)s,mac=%(mac)s,netdev=mgmt '
                        '-netdev user,id=mgmt,%(hostfwdstr)s '
                        '-serial file:%(vmname)s.log '
                        % vars_dict
                        )

            del vars_dict

            for port in vm['ports']:
                tap_id = port['tap_id']
                mac = '00:0a:0a:0a:%02x:%02x' % (vmid, port['port_id'])
                port['mac'] = mac

                command += (
                    '-device %(frontend)s,mac=%(mac)s,netdev=data%(idx)s '
                    '-netdev tap,ifname=%(tap)s,id=data%(idx)s,script=no,'
                    'downscript=no%(vhost)s '
                    % {'mac': mac, 'tap': tap_id, 'idx': port['port_id'],
                       'frontend': vm_frontend,
                       'vhost': ',vhost=on' if self.vhost else ''}
                )

            booting_budget -= 1
            if booting_budget <= 0:
                logger.debug('Sleeping %s secs waiting '
                             'for the VMs to boot', boot_backoff)

                time.sleep(boot_backoff)
                booting_budget = boot_batch_size

            with open('%s/qemu_out_%s' % (self.qemu_logs_dir, vmid), 'w')\
                    as out_file:
                logger.debug('executing >> %s', command)
                self.boot_processes.append(subprocess.Popen(command.split(),
                                                            stdout=out_file))

            vmid += 1

        # Wait for the last batch of VMs to start
        if booting_budget < boot_backoff:
            tsleep = boot_backoff * (boot_batch_size - booting_budget) / \
                                            boot_batch_size
            logger.info('Sleeping %s secs '
                        'waiting for the last VMs to boot',
                        tsleep)
            time.sleep(tsleep)

        # TODO: to be removed, we should loop in the ssh part
        logger.info('Sleeping 5 seconds, just to be on the safe side')
        time.sleep(5)

        self.recover_if_names(experiment)

        logger.info('Experiment has been successfully swapped in.')

    def swap_out(self, experiment):
        """
        :rtype str
        :return: The script to tear down the experiment
        """
        logger.info('Killing qemu processes.')
        # TERM qemu processes
        for process in self.boot_processes:
            process.terminate()

        # Wait for them to shut down
        for process in self.boot_processes:
            process.wait()

        logger.info('Destroying interfaces.')
        port_processes = []
        error_queue = multiprocessing.Queue()
        results_queue = multiprocessing.Queue()
        for vm_name, vm in self.vms.items():
            for port in vm['ports']:
                tap = port['tap_id']
                shim = port['shim']

                commands = []

                commands += ('sudo brctl delif %(br)s %(tap)s\n'
                             'sudo ip link set %(tap)s down\n'
                             'sudo ip tuntap del mode tap name %(tap)s'
                             % {'tap': tap, 'br': shim.name}
                             ).split('\n')
                process = multiprocessing.Process(
                    target=self._run_command_chain,
                    args=(commands, results_queue, error_queue),
                    kwargs={'ignore_errors': True})
                port_processes.append(process)
                process.start()

        total_processes = len(port_processes)
        max_waiting_time = 2 * total_processes
        over_processes = 0

        while max_waiting_time > 0 and over_processes < total_processes:
            # Check for errors
            if not error_queue.empty():
                logger.warning('Failure while shutting down: %s',
                               str(error_queue.get()))
                over_processes += 1
            try:
                # Check for results
                result = results_queue.get(timeout=1)
                if result == "Command chain ran correctly":
                    over_processes += 1
                    logger.debug('%s/%s tear-down port '
                                 'processes completed',
                                 over_processes, total_processes)
            except:
                max_waiting_time -= 1

        error_queue = multiprocessing.Queue()
        results_queue = multiprocessing.Queue()
        shim_processes = []

        for shim in self.shims:
            commands = []
            commands += ('sudo ip link set %(br)s down\n'
                         'sudo brctl delbr %(br)s'
                         % {'br': shim.name}
                         ).split('\n')
            process = multiprocessing.Process(target=self._run_command_chain,
                                              args=(commands,
                                                    results_queue,
                                                    error_queue),
                                              kwargs={'ignore_errors': True})
            shim_processes.append(process)
            process.start()

        total_processes = len(shim_processes)
        max_waiting_time = 2 * total_processes
        over_processes = 0

        while max_waiting_time > 0 and over_processes < total_processes:
            # Check for errors
            if not error_queue.empty():
                logger.warning('Failure while shutting down: %s'
                               % str(error_queue.get()))
                over_processes += 1
            try:
                # Check for results
                result = results_queue.get(timeout=1)
                if result == "Command chain ran correctly":
                    over_processes += 1
                    logger.debug('%s/%s tear-down shim '
                                 'processes completed'
                                 % (over_processes, total_processes))
            except:
                max_waiting_time -= 1
        logger.info('Experiment has been swapped out.')
