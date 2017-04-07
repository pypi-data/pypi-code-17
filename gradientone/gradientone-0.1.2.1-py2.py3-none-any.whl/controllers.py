#!/usr/bin/python

"""

Copyright (C) 2016-2017 GradientOne Inc. - All Rights Reserved
Unauthorized copying or distribution of this file is strictly prohibited
without the express permission of GradientOne Inc.

"""
import collections
import datetime
import imp
import importlib
import json
import logging
import os
import pkgutil
import psutil
import requests
import subprocess
import sys
import time
import multiprocessing as multi
from configparser import ConfigParser
from types import ModuleType
from pkg_resources import DistributionNotFound, get_distribution
from subprocess import Popen, PIPE
from version import __version__
from gateway_helpers import logger, get_headers


cfg = ConfigParser()
cfg.read('/etc/gradient_one.cfg')
COMMON_SETTINGS = cfg['common']
CLIENT_SETTINGS = cfg['client']
BASE_URL = "https://" + COMMON_SETTINGS['DOMAIN']
UPDATE_CHECK_INTERVAL = 10
DEFAULT_PYTHONPATH = '/usr/local/lib/python2.7/dist-packages'
DIRPATH = os.path.dirname(os.path.realpath(__file__))
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
GATEWAY = COMMON_SETTINGS["HARDWARENAME"]
GATEWAY_URL = BASE_URL + '/gateway'


class ClientProcess(multi.Process):
    def __init__(self, *args, **kwargs):
        super(ClientProcess, self).__init__(self, *args, **kwargs)
        self.child_processes = []

    def terminate(self):
        for child_ps in self.child_processes:
            child_ps.terminate()
        super(ClientProcess, self).terminate()


class BaseController(ClientProcess):
    def __init__(self, target=None, name="", keep_alive_interval=600):
        """Initializes the BaseController

        target - the target function for the process this controller
            is managing. Every target function needs to take the
            ClientInfo as the first argument

        name - A client needs to have some identifier that labels it so
            that the controller knows what to start, stop, restart, and
            check for activity. The 'name' should be unique to each
            client. While similar in purpose to pid, the 'name' is
            different in that the same name will be used for each
            restart of a given client, despite new pids being generated
            each time. The 'name' is different from Unix process name
            in that the names here for each client should be unique,
            whereas Unix process names are not. There's no validation
            being done on these names being used, so if you use the
            same name for two different clients in your code you
            will see some strange behavior.

        keep_alive_interval - seconds that target must update the
            activity file within, else this controller will restart
            the target process.
        """
        self.logger = self.get_logger()
        self.target = target
        self.name = name
        self.keep_alive_interval = keep_alive_interval
        self.session = requests.session()
        self.session.headers.update(get_headers())

    def run(self):
        """Main run method, keeps target alive

        Note: This run() method simply runs the 'target' function with
            the 'name' used to initialize the controller. If no
            target or name were given, then nothing will run.

        """
        self.logger.info("Running controller")
        self.keep_alive(self.target, self.name, self.keep_alive_interval)

    def keep_alive(self, target, name, keep_alive_interval=None):
        """Starts and keeps the target process running, or 'alive'

        Rule: If the sub client does not update the activity file for
            its process within the keep_alive_interval, this method
            will restart the client process. Otherwise, if the sub
            client is behaving normally and updating the activity
            file within the required keep_alive_interval, this method
            will log the new activity update from the sub client.

        target - the process that this method is starting and keeping
            alive. This method will pass kwargs 'keep_alive_interval'
            and 'activity_file' for this target process to use to be
            sure to update the activity file within the
            keep_alive_interval.

        name - the name used to keep track of the target process

        keep_alive_interval - the seconds allowed to pass between
            updates to the activity file. If no update is made within
            the keep_alive_interval, this method will restart the
            target process.
        """
        if not keep_alive_interval:
            keep_alive_interval = self.keep_alive_interval
        if not target or not name:
            self.logger.info("Missing target or name")
            return

        activity_file = os.path.join(DIRPATH, name + '_activity.txt')
        kwargs = {
            'keep_alive_interval': keep_alive_interval,
            'activity_file': activity_file,
        }
        self.start_process(target, name=name, ps_kwargs=kwargs)
        latest_activity = "Init"
        while True:
            time.sleep(self.keep_alive_interval)
            filestr = self.read(activity_file)
            if filestr == latest_activity:
                self.logger.warning("No activity since: " + filestr)
                self.restart_process(target, name)
            else:
                self.logger.info("Controller: New activity! %s"
                                 % filestr)
            latest_activity = filestr  # filestr becomes the new last_update

    def read(self, file):
        """Helper function for reading activity files

        If no file, writes current time and returns the time string
        """
        if not os.path.isfile(file):
            c_time = datetime.datetime.now()
            fmt = DATETIME_FORMAT
            time_string = c_time.strftime(fmt)
            with open(file, 'w') as f:
                f.write(time_string)
                return time_string
        with open(file, 'r') as f:
            return f.read(file)

    def write(self, file, content):
        with open(file, 'w') as f:
            f.write(content)

    def start_process(self, target, name, ps_args=(), ps_kwargs={}):
        """Starts a process and saves its pid

        The pid is written to a file, named with the 'name' arg,
        <name>.pid, so with the simple example it's simple.txt.

        The 'name' is used for the Process, the pid file, and the
        activity file relating to the process for the function. The
        convention is <name>_activity.txt, so with the simple example
        this is simple_activity.txt.

        In the run() method of the BaseController, the first arg of
        'args' is the activity file name for the client process to
        update within the keep_alive_interval to prevent the controller
        from restarting the client process.
        """
        ps = ClientProcess(target=target, name=name,
                           args=ps_args, kwargs=ps_kwargs)
        ps.start()
        self.child_processes.append(ps)
        with open(DIRPATH + name + ".pid", "wb") as f:
            f.write(str(ps.pid))

    def stop_process(self, name):
        """Stops the controllers target process"""
        try:
            for child_ps in self.child_processes:
                if child_ps.name == name:
                    child_ps.terminate()
            # with open(DIRPATH + name + ".pid", "rb") as f:
            #     pid = int(f.read())
            # p = psutil.Process(pid)
            # p.terminate()
        except psutil.NoSuchProcess:
            self.logger.info("No " + name + " to stop")
        except Exception:
            self.logger.warning("Unexpected exception stopping " + name,
                                exc_info=True)

    def restart_process(self, target, name, ps_args=()):
        """Stops and starts the client process given a func and name

        The 'name' is used for the Process, the pid file, and the
        activity file relating to the process for the function.
        """
        self.logger.info("Restarting client...")
        self.stop_process(name=name)
        self.start_process(target, name=name, ps_args=ps_args)

    def if_active_pid(self, pid):
        """Check if active unix pid."""
        if psutil.pid_exists(pid):
            return True
        else:
            self.logger.info("The process with pid %s does not exist" % pid)
            return False

    def get_pid_from_name(self, name):
        """Returns the pid for a given client process name.

        The method will check the pid file for the name
        """
        try:
            with open(DIRPATH + name + ".pid", 'r') as f:
                return int(f.read())
        except Exception as e:
            self.logger("get_pid_from_name exception: %s" % e)
            return None

    def get_logger(self, log_filename='controller.log'):
        self.logger = logging.getLogger('controller')
        self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG)
        # create logging handlers
        console_handler = logging.StreamHandler()  # by default, sys.stderr
        file_handler = logging.FileHandler(log_filename)
        # set logging levels
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)
        # add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        return self.logger


class UpdateController(BaseController):
    """Handles running and updating the main client"""
    def __init__(self, *args, **kwargs):
        BaseController.__init__(self, *args, **kwargs)
        version = __version__
        pkg = 'gradientone'
        self.logger.info("Updating to version: %s" % version)
        self.pip_target = self.get_pip_target()
        self.pip_install(pkg, version)
        self.og_client_name = pkg
        self.og_version = version
        self.version = version
        self.prev_version = version
        self.client_name = pkg
        self.client_module = ModuleHelper(pkg).client_module
        self.target = self.client_module.gateway_client.run

    def get_pip_target(self):
        try:
            py_path = os.environ['PYTHONPATH'].split(os.pathsep)
        except KeyError:
            py_path = []
        if not py_path:
            logger.warning("No python path found. Adding default: %s"
                           % DEFAULT_PYTHONPATH)
            sys.path.append(DEFAULT_PYTHONPATH)
            py_path.append(DEFAULT_PYTHONPATH)
        logger.info("PYTHONPATH is %s" % py_path)
        logger.info("Returning pip target as %s" % py_path[0])
        return py_path[0]

    def run(self, update_check_interval=UPDATE_CHECK_INTERVAL):
        """Runs the nanny

        sec_btw_updates - the grace period between updates that the
                          nanny allows the config runner process.
                          Defaults to 600 secs (10 mins)
        """
        self.start_client()
        while True:
            time.sleep(update_check_interval)
            self.check_for_updates()

    def set_version(self, package='gradientone', version=''):
        """Sets current and previous version"""
        if not version:
            version = self.get_pip_show_version(package)
        if self.version == version:
            msg = ("Setting v-%s matches current v-%s. Backup stays as v-%s"
                   % (version, self.version, self.prev_version))
            logger.info(msg)
        else:
            self.prev_version = self.version
            msg = ("New v-%s replacing v-%s. The backup is now: v-%s"
                   % (version, self.version, self.prev_version))
            logger.info(msg)
            self.version = version
            payload = {
                'name': GATEWAY,
                'client_version': version,
                'update_available': False,
                'company': COMMON_SETTINGS['COMPANYNAME'],
            }
            self.session.post(url=GATEWAY_URL, data=json.dumps(payload))

    def get_pip_show_version(self, package='gradientone'):
        """Gets version by parsing pip output"""
        pip_show_pkg = ['pip', 'show', package]
        output = Popen(pip_show_pkg, stdout=PIPE).communicate()[0]
        lines = output.split('\n')
        version = ""
        for line in lines:
            if line.startswith("Version:"):
                version = line.split(':')[1].strip()
        return version

    def pip_install(self, pkg_name='', version=''):
        if not pkg_name:
            pkg_name = self.client_name
        pip_args = ['install', '--upgrade']
        if version:
            logger.info("Installing version: %s" % version)
            pkg_string = pkg_name + '==' + str(version)
            pip_args.append(pkg_string)
        else:
            msg = "No version given. Simply installing " % pkg_name
            logger.info(msg)
            pip_args.append(pkg_name)
        cmd = 'pip ' + ' '.join(pip_args)
        logger.info("Making subprocess.call with %s" % cmd)
        subprocess.call(cmd, shell=True)

    def reload(self, pkg_name='', is_rollback=False, og_install=False):
        if not pkg_name:
            pkg_name = self.client_name
        if self.reload_by_name(pkg_name):
            logger.info("Successfully reloaded %s" % pkg_name)
        else:
            if og_install:
                msg = ("Unable to reload original client! This process will "
                       "continue polling for gateway client software updates."
                       "However, no gateway client that is running may not "
                       "have the latest update running. Restart required.")
                logger.warning(msg)
            elif is_rollback:
                self.install_original()
                self.start_client(og_install=True)
            else:
                response = self.rollback()
                if "Success" in response:
                    self.start_client(is_rollback=True)
                    return
                else:
                    self.install_original()
                    self.start_client(og_install=True)

    def pip_uninstall(self, pkg_name=''):
        if not pkg_name:
            pkg_name = self.client_name
        subprocess.call('pip uninstall', shell=True)

    def install_original(self):
        self.pip_install(self.og_client_name, self.og_version)
        if self.verify_version_info(self.og_client_name, self.og_version):
            msg = ("Successfuly installed original client: %s v-%s"
                   % (self.og_client_name, self.og_version))
            logger.info(msg)
        else:
            msg = ("Failed to install original client: %s v-%s"
                   % (self.og_client_name, self.og_version))
            logger.warning(msg)
        return msg

    def update(self, pkg_name='gradientone', version='',
               force_uninstall=False, is_rollback=False):
        logger.info("Current client version: %s" % self.version)
        if force_uninstall:
            self.pip_uninstall(pkg_name)
        self.pip_install(pkg_name, version)
        if self.verify_version_info(pkg_name, version):
            return "Success! Current version is v-%s" % version
        elif is_rollback:
            logger.warning("Rollback update failed. Installing original")
            return self.install_original()
        else:
            msg = "Update failed"
            logger.warning(msg)
            return msg

    def verify_version_info(self, pkg_name, version=''):
        logger.warning("Verifying version update...")
        v_from_pip_show = self.get_pip_show_version(pkg_name)
        if v_from_pip_show != version:
            msg = ("Verification of v-%s failed. Current version is: v-%s"
                   % (version, v_from_pip_show))
            logger.warning(msg)
            return None
        else:
            logger.warning("Verification of current client v-%s. Success!"
                           % v_from_pip_show)
            self.set_version(pkg_name, v_from_pip_show)
            return True

    def process_update_cmd(self, data):
        """Processes update command from server

        If the update succeeds then the new client is started.
        If the update fails then try a resinstall of current version
        If reinstall of current fails, try rollback to previous
        If rollback to previous fails, try install of original
        and try to start client regardless of og_install result.
        """
        update = collections.defaultdict(str, data)
        if update['new_client_version'] == self.version:
            msg = ("Server version:%s matches client. No action necessary"
                   % update['new_client_version'])
            logger.info(msg)
            return
        # stop client during update process
        self.stop_client()
        if not update['client_package']:
            update['client_package'] = 'gradientone'
        result = self.update(pkg_name=update['client_package'],
                             version=update['new_client_version'])
        if 'Success' in result:
            logger.info("Update: %s" % result)
            self.start_client()
        else:
            # If the update failed. Reinstall current version
            logger.info("Trying re-install of version: %s" % self.version)
            self.pip_install(self.client_name, self.version)
            # Verify the reinstall. If failed, rollback to previous v.
            if self.verify_version_info(self.client_name, self.version):
                self.start_client()
            else:
                result = self.rollback()
                if "Success" in result:
                    logger.info("Rollback: %s" % result)
                    self.start_client(is_rollback=True)
                else:
                    logger.info("Rollback failed. Installing original")
                    result = self.install_original()
                    self.start_client(og_install=True)

    def reload_by_name(self, modname):
        """Safe reload(module) that accepts strings

        Allows str, unicode string, or ModuleType
        """
        if isinstance(modname, str):
            self.logger.info("Getting module from str: %s" % modname)
            self.client_module = ModuleHelper(modname).client_module
        elif isinstance(modname, ModuleType):
            logger.warning("Assigning modname as module")
            self.client_module = modname
        elif isinstance(modname, unicode):
            logger.info("Getting module from unicode: %s" % modname)
            try:
                self.client_module = ModuleHelper(str(modname)).client_module
            except Exception as e:
                logger.warning("Unexpected reload err:%s " % e)
                return None
        else:
            logger.warning("Unexpected modname type:%s" % type(modname))
            return None
        logger.info("Reloading module %s" % self.client_module)
        try:
            imp.reload(self.client_module)
            imp.reload(self.client_module.gateway_helpers)
            imp.reload(self.client_module.gateway_client)
            return True
        except Exception as e:
            logger.warning("Exception during reload: %s" % e)
            return None

    def check_for_updates(self):
        while True:
            time.sleep(UPDATE_CHECK_INTERVAL)
            try:
                url = BASE_URL + '/gateway'
                msg = "Current v " + self.version + " checking:" + url
                logger.info(msg)
                response = self.session.get(url, params={'name': GATEWAY})
                if not response.text:
                    continue
                data = json.loads(response.text)
                if 'update_available' in data and data['update_available']:
                    self.process_update_cmd(data)
            except Exception:
                self.logger.error("Exception in pulling code", exc_info=True)

    def rollback(self):
        logger.info("Rolling back to v-%s" % self.prev_version)
        self.stop_client()
        response = self.update(pkg_name=self.client_name,
                               version=self.prev_version,
                               is_rollback=True)
        return response

    def start_client(self, is_rollback=False, og_install=False):
        logger.info("Starting client: %s v-%s"
                    % (self.client_name, self.version))
        self.reload(self.client_name, is_rollback, og_install)
        try:
            self.start_process(target=self.target, name=self.name)
        except Exception:
            logger.error("Exception in starting client", exc_info=True)
            if og_install:
                msg = ("Unable to start original client! This process will "
                       "continue polling for gateway client software updates."
                       "However, no gateway client is running until a "
                       "successful update happens.")
                logger.warning(msg)
            elif is_rollback:
                self.install_original()
                self.start_client(og_install=True)
            else:
                self.rollback()
                self.start_client(is_rollback=True)

    def stop_client(self):
        logger.info("Stopping client processes")
        try:
            self.stop_process(name=self.name)
        except Exception:
            logger.error("Exception in stopping client", exc_info=True)

    def restart_client(self):
        logger.info("Preparing to restart client....")
        self.stop_client()
        self.start_client()

    def kill_proc_tree(pid, including_parent=False):
        parent = psutil.Process(pid)
        for child in parent.get_children(recursive=True):
            child.kill()
        if including_parent:
            parent.kill()

    def log(self, msg):
        logger.info(msg)

    def get_dist_version(self, package='gradientone'):
        """Gets version using pgk_resources"""
        try:
            _dist = get_distribution(package)
        except DistributionNotFound as e:
            self.version = 'Please install %s' % package
            logger.warning("DistributionNotFound: %s" % e)
        except Exception as e:
            logger.warning("Exception in get_distribution, %s" % e)
            self.version = 'No version info'
        else:
            self.version = _dist.version
            logger.warning("_dist.version: %s" % _dist.version)
        return self.version

    def rreload(self, package, parent_pkg='gradientone'):
        """Recursively reload packages."""
        logger.info("rreload on %s" % package)
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
            logger.info("Found submodule %s (is a package: %s)"
                        % (modname, ispkg))
            modname = parent_pkg + "." + modname
            logger.info("modname: %s" % modname)
            try:
                module = importer.find_module(modname).load_module(modname)
                if ispkg:
                    self.rreload(module, parent_pkg=modname)
                else:
                    self.simple_reload(module)
            except Exception as e:
                msg = "load module %s exc: %s" % (modname, e)
                logger.info(msg)


class ClientInfo(object):
    """Keeps track of basic client process info"""
    def __init__(self, target=None, name="", keep_alive_interval=600,
                 activity_file="", pid=""):
        """Intializes ClientInfo object

        target - the target function for this client
        name - the name to reference this client, should be unique to
            this client.
        keep_alive_interval - the interval that the client must update
            the activity file before the controller will restart the
            client process
        activity_file - the file that needs to be periodically updated
            with update_activity_file()
        pid - the pid of the client process
        """
        self.target = target
        self.name = name
        if not activity_file:
            activity_file = DIRPATH + name + '_activity.txt'
        self.activity_file = activity_file
        self.keep_alive_interval = keep_alive_interval
        self.pid = pid

    @property
    def active(self):
        """If the client process is active or not"""
        if psutil.pid_exists(self.pid):
            return True
        else:
            return False


class MultiClientController(BaseController):
    """Controls multiple client processes

    Attributes:
        clients_dict - a dictionary with a k,v pair for each client this
            controller is in charge of. That k,v pair will have the
            client name for the key and the a ClientInfo object value

        keepers - a dictionary with a k,v paid for each keeper that
            is keeping client processes alive. The key is the same name
            as the client process name with the value: {'pid': ps.pid}
            This is attribute is just for the run_with_sub_masters()
            case. Normal run() usage won't need this.
    """
    def __init__(self, client_infos=[], *args, **kwargs):
        """Initializes MultiClientController

        client_infos is a list of ClientInfo objects that will be
            stored in the 'clients' dictionary attribute

        """
        super(MultiClientController, self).__init__(*args, **kwargs)
        self.clients_dict = collections.defaultdict(str)
        self.keepers = collections.defaultdict(str)
        if not client_infos:
            client_infos = []
            self.logger.warning("No client info for MulitClientController")
        for clt in client_infos:
            try:
                self.clients_dict[clt.name] = clt
            except Exception as e:
                self.logger.info("Controller Init exception e: %s" % e)

    def run(self):
        """Starts the clients and keeps them alive

        First iterates through the ClientInfo objects in the
        clients_dict attribute and starts each client process according
        to the info in the that client's ClientInfo object.

        Then this function runs a loop every 5 seconds that checks the
        activity files of each client process to make sure those
        clients are still updating. If the time (seconds) since the
        last update to a given client's activity file was longer than
        that client's keep_alive_interval then the client process is
        restarted. As part of the restart, the client's activity file
        is updated with the current loop's time (c_time).
        """
        for name in self.clients_dict:
            client = self.clients_dict[name]
            self.start_process(client.target, name=client.name,
                               ps_args=(client,))
        while True:
            for name in self.clients_dict:
                client = self.clients_dict[name]
                c_time = datetime.datetime.now()
                fmt = DATETIME_FORMAT
                act_time_str = self.read(client.activity_file)
                try:
                    act_time = datetime.datetime.strptime(act_time_str, fmt)
                except Exception as e:
                    self.logger.warning("Activity time exception: %s" % e)
                    act_time = c_time
                delta = c_time - act_time
                if delta.total_seconds() > client.keep_alive_interval:
                    self.restart_process(target=client.target, name=name,
                                         ps_args=(client,))
                    self.write(client.activity_file, c_time.strftime(fmt))
            time.sleep(5)

    def run_with_sub_masters(self):
        """Run each client with it's own master keeping it alive"""
        for name in self.clients_dict:
            client = self.clients_dict[name]
            keep_alive_ps_name = name + '_keep_alive'
            keep_alive_args = (client.target, name, client.keep_alive_interval)
            # Starts the process that starts and watches the client process
            self.start_process(self.keep_alive, name=keep_alive_ps_name,
                               ps_args=keep_alive_args)

    def start_process(self, target, name, ps_args=(), ps_kwargs={}):
        """Starts a process and saves its pid

        The pid is written to a file, named with the 'name' arg,
        <name>.pid, so with the simple example it's simple.txt.

        The 'name' is used for the Process, the pid file, and the
        activity file relating to the process for the function. The
        convention is <name>_activity.txt, so with the simple example
        this is simple_activity.txt.

        """
        ps = ClientProcess(target=target, name=name,
                           args=ps_args, kwargs=ps_kwargs)

        ps.start()
        self.child_processes.append(ps)
        self.write(DIRPATH + name + ".pid", str(ps.pid))

    def stop_process(self, name="simple"):
        """Stops the controllers target process"""
        try:
            for child_ps in self.child_processes:
                if child_ps.name == name:
                    child_ps.terminate()
            # with open(DIRPATH + name + ".pid", 'r') as f:
            #     pid = int(f.read())
            # p = psutil.Process(pid)
            # p.terminate()
        except psutil.NoSuchProcess:
            self.logger.info("No " + name + " to stop")
        except Exception:
            self.logger.warning("Unexpected exception stopping " + name,
                                exc_info=True)


class SimpleClient(object):
    def run_example(self, sec_btw_simple_prints=5, activity_file=""):
        """Run example simple client

        If sec_btw_simple_prints is less than the keep_alive_interval,
        that is to say it prints and updates the activity more
        frequently than required by the keep_alive_interval, it will
        simply continue to print indefinitely.

        Else if the sec_btw_simple_prints is greater than the
        keep_alive_interval of the client controller then the
        controller will restart this client. A restart will stop
        this process and start a new process calling this same
        method.
        """
        if not activity_file:
            activity_file = "simple_activity.txt"
        while True:
            msg = "SimpleClient: run at %s" % str(datetime.datetime.now())
            print(msg)
            with open(activity_file, 'w') as f:
                f.write(msg)
            time.sleep(sec_btw_simple_prints)


class SimpleController(BaseController):
    """A controller for examples

        When run() is called by an instance of SimpleController, the
    SimpleClient is run within a keep alive loop. See the
    BaseController run() method for more details
    """
    def __init__(self, *args, **kwargs):
        simple = SimpleClient()
        self.target = simple.run_example
        self.name = 'simple'


class ModuleHelper(object):

    def __init__(self, pkg_name='gradientone'):
        self.client_module = self.get_module(pkg_name)

    def get_module(self, module_name):
        if module_name in sys.modules:
            return sys.modules[module_name]
        else:
            return importlib.import_module(module_name)


def run_example():
    ctrl = SimpleController()
    ctrl.run()
