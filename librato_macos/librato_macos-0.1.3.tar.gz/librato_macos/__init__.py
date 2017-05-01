# Copyright (c) 2017. Librato, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Librato, Inc. nor the names of project contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL LIBRATO, INC. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import time
import logging
import sys
import subprocess
import re
import ast
import socket
import platform
import psutil
import librato

__version__ = "0.1.0"

PREFIX = 'demo.librato.'

class MACOSAgent(object):
    """
    This is the main class for the MAC OS Agent
    """
    resolution = 60
    hostname = socket.gethostname()
    min_pid_lifetime = 120
    default_tags = {}
    username = ""
    token = ""

    def __init__(self, **kwargs):
        level = logging.ERROR
        if 'log_level' in kwargs:
            if kwargs['log_level'] == logging.DEBUG:
                level = logging.DEBUG
        logging.basicConfig(format="%(asctime)s (%(levelname)s) librato-macos : " + \
                       "%(message)s", level=level)
        logging.debug("Initializing Agent")

        try:
            config_file = open(os.environ['HOME'] + '/.librato-macos', 'r')
        except IOError:
            logging.error( "Config file does not exist at %s.  Please add a config file there to continue." % (os.environ['HOME'] + '/.librato-macos'))
            exit(1)
        for line in config_file:
            if line[0] is not "#" and line is not "":
                param = line.rstrip('\n').split('=')
                if param[0] == "LIBRATO_USERNAME":
                    self.username = param[1]
                elif param[0] == "LIBRATO_TOKEN":
                    self.token = param[1]
                elif param[0] == 'LIBRATO_DEFAULT_TAGS':
                    try:
                        self.default_tags = ast.literal_eval(param[1])
                    except Exception as e:
                        logging.debug("Error parsing default tags: %s" % e)
                        logging.debug("Default tags will be empty")
                elif param[0] == 'LIBRATO_HOSTNAME':
                    self.hostname = param[1]
                elif param[0] == 'LIBRATO_RESOLUTION':
                    try:
                        self.resolution = int(param[1])
                    except ValueError:
                        logging.debug( "Resolution is not set to a valid value: %s" % param[1])
                        logging.debug( "Resolution will remain at 60")
                elif param[0] == 'LIBRATO_PID_TIMEOUT':
                    try:
                        self.min_pid_lifetime = int(param[1])
                    except ValueError:
                        logging.debug( "minimum pid lifetime is not set to a valid value: %s" % param[1])
                        logging.debug( "minimum pid lifetime will remain at 120")

    def api(self):
        api = librato.connect(self.username, self.token)
        api.custom_ua = "librato_macos/" + __version__
        return api

    def merge_two_dicts(self, dict1, dict2):
        """Given two dicts, merge them into a new dict as a shallow copy.
        :param dict1: A dictionary to merge
        :type dict1: dict
        :param dict2: Another dictionary to merge
        :type dict2: dict
        """
        return_dict = dict1.copy()
        return_dict.update(dict2)
        return return_dict


    def get_ioreg_attr(self, device, attr_list):
        """
        Given a device name and a list of attributes,
        return a dict that contains the desired attributes
        from running ioreg command (mac only)
        """
        data = {}
        command = "ioreg -rn %s" % device
        try:
            device_data = subprocess.check_output(
                command, stderr=subprocess.STDOUT,
                shell=True).decode('latin-1').encode('utf-8').splitlines()
        except Exception as e:
            logging.error("Unable to retrieve data for %s: %s" % (device, e))
            return data
        for attr in device_data:
            attr = str(attr)
            pair = attr.replace("|", '').replace("b'","").replace("\"", "").strip().split("=")
            try:
                ndx = attr_list.index(str(pair[0].strip()))
                if ndx >= 0:
                    data[attr_list[ndx]] = pair[1].strip()
            except ValueError:
                pass
            except Exception as e:
                logging.error("There was an error processing ioreg: %s" % e)

        return data

    def generate_measurements(self, measure_time, processes):
        """
        Generate measurements based of the local machine
        """
        os_type = platform.system().lower()
        if os_type != 'darwin':
            logging.error("Only Mac OS is supported at this time")
            exit(1)
        version = platform.mac_ver()[0]
        api = self.api()
        q = api.new_queue()

        #platform
        default_tags = self.merge_two_dicts(
            {'host': self.hostname, 'os_type': os_type, 'version': version}, self.default_tags
            )

        #cpu metrics
        cpu_percentages = psutil.cpu_times_percent(interval=1, percpu=False)
        for key in cpu_percentages._fields:
            q.add(
                PREFIX + "cpu.percent." + key,
                getattr(cpu_percentages, key),
                tags=default_tags, time=measure_time)

        #load
        load = os.getloadavg()
        q.add(PREFIX + "load.load.shortterm", load[0], tags=default_tags, time=measure_time)
        q.add(PREFIX + "load.load.midterm", load[1], tags=default_tags, time=measure_time)
        q.add(PREFIX + "load.load.longterm", load[2], tags=default_tags, time=measure_time)


        #disk metrics
        disk = psutil.disk_usage('/')
        q.add(PREFIX + "df.percent_bytes.free", disk.percent, tags=default_tags, time=measure_time)

        disk_counters = psutil.disk_io_counters(perdisk=True)
        for k in disk_counters:
            q.add(
                PREFIX + "disk.disk_ops.read",
                disk_counters[k].read_count,
                tags=self.merge_two_dicts({'disk': k}, default_tags),
                time=measure_time)
            q.add(
                PREFIX + "disk.disk_ops.write",
                disk_counters[k].write_count,
                tags=self.merge_two_dicts({'disk': k}, default_tags),
                time=measure_time)

        #memory metrics
        virtual_mem = psutil.virtual_memory()
        q.add(PREFIX + "memory.memory.free", virtual_mem.free, tags=default_tags, time=measure_time)
        q.add(PREFIX + "memory.memory.used", virtual_mem.used, tags=default_tags, time=measure_time)
        q.add(
            PREFIX + "memory.memory.buffered",
            getattr(virtual_mem, "buffers", 0),
            tags=default_tags,
            time=measure_time)
        q.add(
            PREFIX + "memory.memory.cached",
            getattr(virtual_mem, "cached", 0),
            tags=default_tags,
            time=measure_time)
        swap_mem = psutil.swap_memory()
        q.add(PREFIX + "swap.swap.free", swap_mem.free, tags=default_tags, time=measure_time)
        q.add(PREFIX + "swap.swap.used", swap_mem.used, tags=default_tags, time=measure_time)

        #network stats
        network_io = psutil.net_io_counters(pernic=True)
        for k in network_io:
            q.add(
                PREFIX + "interface.if_octets.rx",
                network_io[k].bytes_recv,
                tags=self.merge_two_dicts({'interface': k}, default_tags),
                time=measure_time)
            q.add(
                PREFIX + "interface.if_octets.tx",
                network_io[k].bytes_sent,
                tags=self.merge_two_dicts({'interface': k}, default_tags),
                time=measure_time)
            q.add(
                PREFIX + "interface.if_packets.rx",
                network_io[k].packets_recv,
                tags=self.merge_two_dicts({'interface': k}, default_tags),
                time=measure_time)
            q.add(
                PREFIX + "interface.if_packets.tx",
                network_io[k].packets_sent,
                tags=self.merge_two_dicts({'interface': k}, default_tags),
                time=measure_time)


        #pids
        pids = psutil.pids()
        active_process = []
        for pid in pids:
            try:
                p = psutil.Process(pid)
                process_tags = self.merge_two_dicts(
                    {
                        'pid_username': p.username(),
                        'pid': pid,
                        'pid_name': p.name(),
                        'parent': p.parent().pid
                    },
                    default_tags)
                cpu_percent = p.cpu_percent(interval=.1)
                cpu_times = p.cpu_times()
                memory_percent = p.memory_percent()
                #filter out short lived processes
                if p.name() not in active_process and (time.time() - p._create_time) > self.min_pid_lifetime:
                    active_process.append(p.name())
                q.add(
                    PREFIX + "pids.pid.cpu_percentage",
                    cpu_percent,
                    tags=process_tags,
                    time=measure_time)
                q.add(
                    PREFIX + "pids.pid.memory_percentage",
                    memory_percent,
                    tags=process_tags,
                    time=measure_time)
                q.add(
                    PREFIX + "pids.pid.cpu_time.seconds",
                    cpu_times.user + cpu_times.system,
                    tags=process_tags,
                    time=measure_time)

            except Exception as e:
                logging.debug("permissions error or pid died")

        #annotate on kill
        if len(processes) > 0:
            killed = [a for a in processes+active_process if (a in processes) and (a not in active_process)]
            for pid in killed:
                api.post_annotation("pid-killed",
                    title=pid,
                    start_time=measure_time,
                    description="%s was killed" % pid)

        #wireless
        wireless = subprocess.check_output(
            "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I",
            stderr=subprocess.STDOUT,
            shell=True).decode('utf8').splitlines()
        wireless_running = False
        for attr in wireless:
            pair = attr.strip().split(':')
            if pair[0] == "agrCtlRSSI":
                signal_strength = int(pair[1].replace(' -', ""))
            elif pair[0] == "agrCtlNoise":
                signal_noise = int(pair[1].replace(' -', ""))
            elif pair[0] == "SSID":
                wireless_running = True
                SSID = pair[1].replace(' ', "")
        if wireless_running:
            wireless_tags = self.merge_two_dicts({'ssid': SSID}, default_tags)
            q.add(
                PREFIX + "wifi.signal.strength",
                signal_strength,
                tags=wireless_tags,
                time=measure_time)
            q.add(PREFIX + "wifi.signal.noise", signal_noise, tags=wireless_tags, time=measure_time)

        #battery mouse, keyboard, machine
        wireless_mouse = self.get_ioreg_attr("BNBMouseDevice", ["Product", "BatteryPercent"])
        wireless_keyboard = self.get_ioreg_attr("AppleBluetoothHIDKeyboard", ["Product", "BatteryPercent"])
        smart_battery = self.get_ioreg_attr("AppleSmartBattery", ["MaxCapacity", "CurrentCapacity"])

        non_decimal = re.compile(r'[^\d.]+')
        for device in [wireless_mouse, wireless_keyboard]:
            if device != {}:
                product = 'invalid_name'
                try:
                    product = device['Product'].decode('latin-1').encode('ascii', errors='replace').replace("?", "_")
                except Exception:
                    pass
                q.add(
                    PREFIX + "energy.battery.percent",
                    non_decimal.sub('',device['BatteryPercent']),
                    tags=self.merge_two_dicts(
                        {'device': product}, default_tags
                        ),
                    time=measure_time)

        if smart_battery != {}:
            current_capacity = non_decimal.sub('', smart_battery['CurrentCapacity'])
            max_capacity = non_decimal.sub('', smart_battery['MaxCapacity'])
            q.add(
                PREFIX + "energy.battery.percent",
                (
                    float(current_capacity) /
                    float(max_capacity)
                ) * 100.00,
                tags=self.merge_two_dicts(
                    {'device': 'smart battery'}, default_tags),
                time=measure_time)



        #submit all measurements
        logging.info("Submiting metrics at %d" % measure_time)
        try:
            q.submit()
        except Exception as e:
            logging.error("Could not post metrics to Librato cause: %s" % e)
        return active_process

    def run(self):
        measure_time = time.time()
        #get tick on resolution
        print("Waiting for syncing on the 60 second mark")
        time.sleep(self.resolution - (measure_time % self.resolution))
        measure_time += (self.resolution - (measure_time % self.resolution))
        processes = []
        while True:
            print("preparing data for transmission")
            processes = self.generate_measurements(measure_time, processes)
            print("data sent for timestamp %d" % measure_time)
            measure_time += self.resolution
            sleep_time = measure_time - time.time()
            # if the Mac goes to sleep, it will cause measure_time
            #   to be < current_time
            if sleep_time < 0:
                sleep_time = self.resolution - (time.time() % self.resolution)
            print("Sleeping until next minute mark")
            time.sleep(sleep_time)

    def create_spaces(self):
        api = self.api()

        base_name = self.username.split('@')[0].split('+')[0]
        space_name = "Demo Overview (%s)" % base_name
        pids_name = "PIDS Demo (%s)" % base_name

        space = api.find_space(space_name)
        pids_space = api.find_space(pids_name)

        if not space or not pids_space:
            qp = {"type":"gauge", "period":60}
            api._mexe("metrics/demo.librato.cpu.percent.idle", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.cpu.percent.nice", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.cpu.percent.system", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.cpu.percent.user", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.df.percent_bytes.free", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.disk.disk_ops.read", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.disk.disk_ops.write", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.energy.battery.percent", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.interface.if_octets.rx", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.interface.if_octets.tx", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.interface.if_packets.rx", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.interface.if_packets.tx", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.load.load.longterm", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.load.load.midterm", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.load.load.shortterm", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.memory.memory.buffered", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.memory.memory.cached", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.memory.memory.free", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.memory.memory.used", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.pids.pid.cpu_percentage", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.pids.pid.cpu_time.seconds", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.pids.pid.memory_percentage", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.swap.swap.free", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.swap.swap.used", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.wifi.signal.noise", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.wifi.signal.strength", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.wireless.signal.noise", method="PUT", query_props=qp)
            api._mexe("metrics/demo.librato.wireless.signal.strength", method="PUT", query_props=qp)
            api.post_annotation("pid-killed",
                title="Installed librato-macos")

        if not pids_space:
            pids_space = api.create_space(pids_name, tags=True)

            chart = api.create_chart('PIDS CPU percentage', pids_space, type='line', streams=[{'tags': [{u'grouped': False, u'dynamic': True, u'name': u'host'}, {u'grouped': False, u'dynamic': True, u'name': u'os_type'}, {u'grouped': False, u'dynamic': True, u'name': u'parent'}, {u'grouped': False, u'dynamic': True, u'name': u'pid'}, {u'grouped': False, u'dynamic': True, u'name': u'version'}, {u'grouped': False, u'dynamic': True, u'name': u'pid_username'}, {u'grouped': True, u'values': [], u'name': u'pid_name'}], 'composite': u'filter(s("demo.librato.pids.pid.cpu_percentage", "%"), {gt:"1",function:"mean"})', 'split_axis': False, 'summary_function': u'sum', 'position': 0, 'type': u'composite'}])
            chart = api.create_chart('PIDS Memory Usage', pids_space, type='line', streams=[{'tags': [{u'grouped': False, u'dynamic': True, u'name': u'host'}, {u'grouped': False, u'dynamic': True, u'name': u'os_type'}, {u'grouped': False, u'dynamic': True, u'name': u'parent'}, {u'grouped': False, u'dynamic': True, u'name': u'pid'}, {u'grouped': False, u'dynamic': True, u'name': u'version'}, {u'grouped': False, u'dynamic': True, u'name': u'pid_username'}, {u'grouped': True, u'values': [], u'name': u'pid_name'}], 'composite': u'filter(s("demo.librato.pids.pid.memory_percentage", "%"), {gt:"1",function:"mean"})', 'split_axis': False, 'summary_function': u'sum', 'position': 0, 'type': u'composite'}])            
            chart = api.create_chart('PIDS Run Time', pids_space, type='line', streams=[{'tags': [{u'grouped': False, u'dynamic': True, u'name': u'host'}, {u'grouped': False, u'dynamic': True, u'name': u'os_type'}, {u'grouped': False, u'dynamic': True, u'name': u'parent'}, {u'grouped': False, u'dynamic': True, u'name': u'pid'}, {u'grouped': False, u'dynamic': True, u'name': u'version'}, {u'grouped': False, u'dynamic': True, u'name': u'pid_username'}, {u'grouped': True, u'values': [], u'name': u'pid_name'}], 'composite': u'filter(s("demo.librato.pids.pid.cpu_time.seconds", "%"), {gt:"100",function:"mean"})', 'split_axis': False, 'summary_function': u'sum', 'position': 0, 'type': u'composite', 'transform_function': u'x/3600'}])
 
        if not space:
            space = api.create_space(space_name, tags=True)

            chart = api.create_chart('CPU', space, type='line', max='100.0', min='0.0', streams=[{'tags': [{u'dynamic': True, u'name': u'host'}, {u'grouped': False, u'dynamic': True, u'name': u'os_type'}, {u'grouped': False, u'dynamic': True, u'name': u'version'}], 'composite': u'\ngroup_by("host",\n  subtract(\n    [\n      sum(s("demo.librato.cpu.percent.*", "%")),\n      s("demo.librato.cpu.percent.idle", "%")\n    ]\n  )\n)\n', 'split_axis': False, 'units_long': u'Utilization(%)', 'summary_function': u'average', 'units_short': u'util %', 'position': 0, 'downsample_function': u'average', 'type': u'composite'}, {'metric': u'pid-killed', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 1, 'type': u'annotation'}])
            chart = api.create_chart('Load (short-term)', space, type='line', streams=[{'tags': [{u'grouped': False, u'dynamic': True, u'name': u'version'}, {u'grouped': False, u'dynamic': True, u'name': u'host'}, {u'grouped': False, u'dynamic': True, u'name': u'os_type'}], 'metric': u'demo.librato.load.load.shortterm', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 0, 'type': u'gauge', 'group_function': u'average'}, {'metric': u'pid-killed', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 1, 'type': u'annotation'}])
            chart = api.create_chart('Process Count', space, type='bignumber', related_space=pids_space.id, use_last_value='True', streams=[{'tags': [{u'grouped': False, u'dynamic': True, u'name': u'os_type'}, {u'grouped': False, u'dynamic': True, u'name': u'host'}, {u'grouped': False, u'dynamic': True, u'name': u'version'}], 'metric': u'demo.librato.pids.pid.cpu_percentage', 'split_axis': False, 'source': u'*', 'summary_function': u'count', 'position': 0, 'type': u'gauge', 'group_function': u'sum'}])
            chart = api.create_chart('Battery Level', space, type='bignumber', use_last_value='True', thresholds=[{ "operator":"<", "value":15, "type":"red"}, { "operator":"<", "value":30, "type":"yellow"}], streams=[{'tags': [{u'grouped': False, u'dynamic': True, u'name': u'os_type'}, {u'grouped': False, u'dynamic': True, u'name': u'version'}, {u'grouped': False, u'values': [u'smart battery'], u'name': u'device'}, {u'grouped': False, u'dynamic': True, u'name': u'host'}], 'metric': u'demo.librato.energy.battery.percent', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 0, 'type': u'gauge', 'group_function': u'average'}])
            chart = api.create_chart('Disk Read Ops', space, type='line', streams=[{'tags': [{u'grouped': False, u'dynamic': True, u'name': u'host'}], 'composite': u'rate(derive(s("demo.librato.disk.disk_ops.read", "%"), {detect_reset: "true"}))', 'split_axis': False, 'units_long': u'Ops / sec', 'summary_function': u'average', 'units_short': u'ops/sec', 'position': 0, 'downsample_function': u'average', 'type': u'composite'}, {'metric': u'pid-killed', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 1, 'type': u'annotation'}])
            chart = api.create_chart('Disk Write Ops', space, type='line', streams=[{'tags': [{u'grouped': False, u'dynamic': True, u'name': u'host'}, {u'grouped': False, u'dynamic': True, u'name': u'os_type'}, {u'grouped': False, u'dynamic': True, u'name': u'version'}], 'composite': u'rate(derive(s("demo.librato.disk.disk_ops.write", "%"), {detect_reset: "true"}))', 'split_axis': False, 'units_long': u'Ops / sec', 'summary_function': u'average', 'units_short': u'ops/sec', 'position': 0, 'downsample_function': u'average', 'type': u'composite'}, {'metric': u'pid-killed', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 1, 'type': u'annotation'}])
            chart = api.create_chart('Wifi Signal Strength', space, type='bignumber', use_last_value='True', thresholds=[{ "operator":"<", "value":50, "type":"red"}, { "operator":"<", "value":75, "type":"yellow"}], streams=[{'tags': [{u'grouped': False, u'dynamic': True, u'name': u'version'}, {u'grouped': False, u'dynamic': True, u'name': u'host'}, {u'grouped': False, u'dynamic': True, u'name': u'os_type'}], 'metric': u'demo.librato.wifi.signal.strength', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 0, 'type': u'gauge', 'group_function': u'average'}])
            chart = api.create_chart('Wifi Signal Noise', space, type='bignumber', use_last_value='True', thresholds=[{ "operator":">", "value":90, "type":"red"}, { "operator":">", "value":70, "type":"yellow"}], streams=[{'metric': u'demo.librato.wifi.signal.noise', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 0, 'type': u'gauge', 'group_function': u'average'}])
            chart = api.create_chart('Memory Free', space, type='line', streams=[{'tags': [{u'grouped': False, u'dynamic': True, u'name': u'version'}, {u'grouped': False, u'dynamic': True, u'name': u'host'}, {u'grouped': False, u'dynamic': True, u'name': u'os_type'}], 'type': u'gauge', 'metric': u'demo.librato.memory.memory.free', 'period': 60, 'split_axis': False, 'source': u'*', 'group_function': u'average', 'units_short': u'GB', 'position': 0, 'summary_function': u'average', 'transform_function': u'x / 1024 / 1024 / 1024'}, {'metric': u'pid-killed', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 1, 'type': u'annotation'}])
            chart = api.create_chart('Memory Used', space, type='line', streams=[{'tags': [{u'grouped': False, u'dynamic': True, u'name': u'version'}, {u'grouped': False, u'dynamic': True, u'name': u'os_type'}, {u'grouped': False, u'dynamic': True, u'name': u'host'}], 'type': u'gauge', 'metric': u'demo.librato.memory.memory.used', 'period': 60, 'split_axis': False, 'source': u'*', 'group_function': u'average', 'units_short': u'GB', 'position': 0, 'summary_function': u'average', 'transform_function': u'x / 1024 / 1024 / 1024'}, {'metric': u'pid-killed', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 1, 'type': u'annotation'}])
            chart = api.create_chart('Peripheral Battery Life', space, type='line', streams=[{'tags': [{u'grouped': True, u'values': [u'!smart battery', u'*'], u'name': u'device'}, {u'grouped': False, u'dynamic': True, u'name': u'host'}, {u'grouped': False, u'dynamic': True, u'name': u'os_type'}, {u'grouped': False, u'dynamic': True, u'name': u'version'}], 'metric': u'demo.librato.energy.battery.percent', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 0, 'type': u'gauge', 'group_function': u'average'}, {'metric': u'pid-killed', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 1, 'type': u'annotation'}])
            chart = api.create_chart('Network Traffic In', space, type='stacked', streams=[{'tags': [{u'dynamic': True, u'name': u'host'}, {u'grouped': False, u'dynamic': True, u'name': u'os_type'}, {u'grouped': False, u'dynamic': True, u'name': u'version'}], 'composite': u'rate(\n  scale(\n    scale(\n      derive(s("demo.librato.interface.if_octets.rx", "%"), {detect_reset: "true"}),\n      {factor:"1/1000000"}\n    ),\n    {factor:"8"}\n  )\n)', 'split_axis': False, 'units_long': u'Mbps', 'summary_function': u'average', 'units_short': u'mbps', 'position': 0, 'downsample_function': u'average', 'type': u'composite'}, {'metric': u'pid-killed', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 1, 'type': u'annotation'}])
            chart = api.create_chart('Network Packets In', space, type='stacked', streams=[{'tags': [{u'dynamic': True, u'name': u'host'}, {u'grouped': False, u'dynamic': True, u'name': u'os_type'}, {u'grouped': False, u'dynamic': True, u'name': u'version'}], 'composite': u'rate(derive(s("demo.librato.interface.if_packets.rx", "%"), {detect_reset: "true"}))', 'split_axis': False, 'units_long': u'Packets/sec', 'summary_function': u'average', 'units_short': u'pps', 'position': 0, 'downsample_function': u'average', 'type': u'composite'}, {'metric': u'pid-killed', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 1, 'type': u'annotation'}])
            chart = api.create_chart('Network Traffic Out', space, type='stacked', streams=[{'tags': [{u'dynamic': True, u'name': u'host'}, {u'grouped': False, u'dynamic': True, u'name': u'os_type'}, {u'grouped': False, u'dynamic': True, u'name': u'version'}], 'composite': u'rate(\n  scale(\n    scale(\n      derive(s("demo.librato.interface.if_octets.tx", "%"), {detect_reset: "true"}),\n      {factor:"1/1000000"}\n    ),\n    {factor:"8"}\n  )\n)', 'split_axis': False, 'units_long': u'Mbps', 'summary_function': u'average', 'units_short': u'mbps', 'position': 0, 'downsample_function': u'average', 'type': u'composite'}, {'metric': u'pid-killed', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 1, 'type': u'annotation'}])
            chart = api.create_chart('Network Packets Out', space, type='stacked', streams=[{'tags': [{u'dynamic': True, u'name': u'host'}, {u'grouped': False, u'dynamic': True, u'name': u'os_type'}, {u'grouped': False, u'dynamic': True, u'name': u'version'}], 'composite': u'rate(derive(s("demo.librato.interface.if_packets.tx", "%"), {detect_reset: "true"}))', 'split_axis': False, 'units_long': u'Packets/sec', 'summary_function': u'average', 'units_short': u'pps', 'position': 0, 'downsample_function': u'average', 'type': u'composite'}, {'metric': u'pid-killed', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 1, 'type': u'annotation'}])
            chart = api.create_chart('Disk Free %', space, type='line', streams=[{'tags': [{u'grouped': False, u'dynamic': True, u'name': u'version'}, {u'grouped': False, u'dynamic': True, u'name': u'host'}, {u'grouped': False, u'dynamic': True, u'name': u'os_type'}], 'metric': u'demo.librato.df.percent_bytes.free', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 0, 'type': u'gauge', 'group_function': u'average'}, {'metric': u'pid-killed', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 1, 'type': u'annotation'}])
            chart = api.create_chart('Swap Free', space, type='line', streams=[{'tags': [{u'grouped': False, u'dynamic': True, u'name': u'os_type'}, {u'grouped': False, u'dynamic': True, u'name': u'version'}, {u'grouped': False, u'dynamic': True, u'name': u'host'}], 'type': u'gauge', 'metric': u'demo.librato.swap.swap.free', 'period': 60, 'split_axis': False, 'source': u'*', 'group_function': u'average', 'units_short': u'GB', 'position': 0, 'summary_function': u'average', 'transform_function': u'x / 1024 / 1024 / 1024'}, {'metric': u'pid-killed', 'split_axis': False, 'source': u'*', 'summary_function': u'average', 'position': 1, 'type': u'annotation'}])
        return [space.id, pids_space.id]
