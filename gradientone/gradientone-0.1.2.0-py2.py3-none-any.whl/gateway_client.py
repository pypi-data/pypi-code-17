#!/usr/bin/env python


"""

Copyright (C) 2016-2017 GradientOne Inc. - All Rights Reserved
Unauthorized copying or distribution of this file is strictly prohibited
without the express permission of GradientOne Inc.

"""

import collections
import datetime
import json
import multiprocessing as multi
import os
from threading import Thread
from Queue import Queue

try:
    from urllib.parse import urljoin
except:
    from urlparse import urljoin

import psutil
import time
import traceback
from configparser import ConfigParser
from subprocess import Popen
import requests
import gateway_helpers
import misc_scope
import tek_grl_configs
import test_runners
from device_drivers import usb_controller

# from matlab_conversion import process_conversion_request
import schema_forms

cfg = ConfigParser()
cfg.read('/etc/gradient_one.cfg')
COMMON_SETTINGS = cfg['common']
CLIENT_SETTINGS = cfg['client']

SENTRY_CLIENT = gateway_helpers.get_sentry()

INSTRUMENTS = gateway_helpers.get_usbtmc_devices()+gateway_helpers.get_copley_devices()  # noqa
SECONDS_BTW_HEALTH_POSTS = 15
CLIENT_ID = 'ORIGINAL'
SAMPLE_FILE = 'MDO30121M.txt'
if COMMON_SETTINGS['DOMAIN'].find("localhost") == 0 or COMMON_SETTINGS['DOMAIN'].find("127.0.0.1") == 0:  # noqa
    BASE_URL = "http://"+COMMON_SETTINGS['DOMAIN']
else:
    BASE_URL = "https://" + COMMON_SETTINGS['DOMAIN']
CONFIG_URL = BASE_URL + '/commands'
logger = gateway_helpers.logger


class ConfigManager(object):
    """Manages config related client workflow"""
    def __init__(self):
        self.session = requests.session()
        self.setup_q = Queue()
        self.order_processor = OrderProcessor(self.session, self.setup_q)

    """Manages configs for instruments from the server"""
    def check_config_url(self):
        """polls the configuration URL for a test run object"""
        config_url = CONFIG_URL
        headers = gateway_helpers.get_headers()
        params = {'status': 'pending', 'command_index': 0}
        response = self.session.get(config_url, headers=headers, params=params)
        if response.status_code == 401:
            headers = gateway_helpers.get_headers(refresh=True)
            response = self.session.get(config_url, headers=headers)
        if response:
            self.process_response(response)
        else:
            logger.error("No response from server")

    def check_for_configs(self):
        logger.info("Starting checks for configs")
        update_timer = 0
        while True:
            try:
                self.check_config_url()
            except Exception:
                logger.warning("check_config_url exception", exc_info=True)
                SENTRY_CLIENT.captureException()
            time.sleep(1)
            update_timer += 1
            if update_timer == 10:  # updates counter file 10sec intervals
                update_timer = 0
                update_counter_file()

    def start_threads(self):
        """Runs the config manager indefinitely

        Two threads run until gateway_client is stopped

        1. Check_url_thread looks for new configs
        2. OrderProcessor that handles the config orders
        """
        cct = Thread(target=self.check_for_configs, name="check_config")
        prt = Thread(target=self.order_processor.start,
                     name="process_orders")
        cct.start()
        prt.start()
        cct.join()
        prt.join()

    def process_response(self, response):
        """Processes response from server to config get requests

        Checks if command is a Config or Capture before running.

        Else checks if it's 'check_scope'
        Else checks if it's some other Special command
        Else it considers the response a no command
        # ToDo - add a case for unrecognised commands in response
        """
        try:
            command = collections.defaultdict(str, json.loads(response.text))
        except Exception as e:
            logger.warning("Exception loading setup data, e:%s" % e)
            return
        logger.debug("Setup received: %s" % command)
        kind = command['category']
        if kind == 'Config' or kind == 'Capture':
            logger.info("%s Command received: %s" % (kind, command))
            # self.setup_q.put(command)
            test_runner = test_runners.TestRunner(self.session)
            test_runner.run_command(command)
        # most commands will be test runs like above
        # special commands and continue commands below
        elif command['arg'] == 'check_scope':
            scope_info = None
            try:
                instrument_type = command['instrument_type']
                scope_info = misc_scope.check_scope(instrument_type)
            except Exception:
                logger.error(traceback.format_exc())
                SENTRY_CLIENT.captureException()
            finally:
                gateway_helpers.post_alert(scope_info)
        elif command['category'] == 'Special':
            self.process_special_command(command)
        # If the response from the server has no orders or commands
        else:
            logger.info("No command; Time:" + str(datetime.datetime.now()) +
                        "; Gateway:" + COMMON_SETTINGS['HARDWARENAME'] +
                        "; Company:" + COMMON_SETTINGS['COMPANYNAME'] +
                        "; Domain:" + COMMON_SETTINGS['DOMAIN'])

    def process_special_command(self, command):
        """Runs special commands not associated with an instrument run"""
        setup = command
        spc = setup['special_command']
        logger.info("Special command found: %s" % spc)
        if spc == 'reset' or spc == 'check':
            misc_scope.check_or_reset(self.session, spc, setup[
                'instrument_type'])
        elif spc == 'reset_usb':
            gateway_helpers.reset_device_with_tag()
        elif spc == 'UsbRawInputCommand':
            usb_contr = usb_controller.UsbController()
            instr = usb_contr.get_instrument(setup['mnf_id'], setup['dev_id'])
            logger.info("issuing command %s" % setup['usb_command'])
            resp = usb_contr.ask(instr, setup['usb_command'])
            logger.info(resp)
        elif spc == 'grl-test':
            logger.info("starting grl-test")
            grl = tek_grl_configs.Grl_Test()
            resp = grl.run_grl_test()
            logger.info("grl test response: %s" % resp)
            gateway_helpers.post_alert(self.session, {'grl_test': resp})
        else:
            logger.warning("unknown special command: %s" % command)
            gateway_helpers.post_alert(self.session, {'unknown_command': spc})


def update_counter_file():
    """Updates counter for nanny to check"""
    with open("counter_file.txt", "w") as counter_file:
        counter_file.write("Last run at %s" % str(datetime.datetime.now()))


def config_gets():
    """Starts the manager for getting and running configs"""
    logger.info("updating counter file in config_gets")
    update_counter_file()
    logger.info("initializing ConfigManager in config_gets")
    cfg_manager = ConfigManager()
    cfg_manager.check_for_configs()
    # cfg_manager.start_threads()  # for multi-threaded command processing


class HealthManager(object):
    def __init__(self):
        self.session = requests.session()
        headers = gateway_helpers.get_headers()
        self.session.headers.update(headers)

    """Manages process that posts gateway health info"""
    def post_health_data(self):
        """posts the health data to server for logging"""
        health_url = BASE_URL + '/gateway/health'
        payload = {
            "instruments": INSTRUMENTS,
            "gateway": COMMON_SETTINGS['HARDWARENAME'],
        }
        data = json.dumps(payload)
        logger.info("Posting to: %s with data: %s" % (health_url, data))
        self.session.post(health_url, data=data)

    def run(self):
        """Runs the health manager indefinitely"""
        while True:
            try:
                self.post_health_data()
            except Exception:
                logger.info("post health data exception", trace=True)
                SENTRY_CLIENT.captureException()
            time.sleep(SECONDS_BTW_HEALTH_POSTS)


def health_posts():
    """Runs the manager that posts gateway health info"""
    with open("health_posts.pid", "w") as f:
        f.write(str(os.getpid()))
    health_manager = HealthManager()
    health_manager.run()


class GatewayManager(object):
    """Manages the gateway itself"""
    def request_commands(self):
        """Polls the command URL for a commands that control the NUC"""
        command_url = (BASE_URL +
                       "/get_nuc_commands/" + COMMON_SETTINGS['COMPANYNAME'] +
                       "/" + COMMON_SETTINGS['HARDWARENAME'] + "/" + CLIENT_ID)
        response = gateway_helpers.authorize_and_get(command_url)
        command = response.text
        if command != 'None':
            logger.info("command received: " + command)
        else:
            command = None
        return command

    def command_handler(self, config_gets, health_posts, conversion_gets):
        """Handles ad hoc commands for gateway"""
        new_client_proc = None
        while True:
            command = self.request_commands()
            if not command:
                log_statement = "COMMAND PROCESSOR LOG: No command at "
                log_statement += str(datetime.datetime.now())
                logger.info(log_statement)
            elif command == "start_conversion_checks":
                conversion_gets.start()
            elif command == "stop_conversion_checks":
                conversion_gets.terminate()
            elif command == "start_test_run_checks":
                config_gets.start()
            elif command == "stop_test_run_checks":
                config_gets.terminate()
            elif command == "start_health_posts":
                health_posts_ps = multi.Process(target=health_posts)
                health_posts_ps.start()
            elif command == "stop_health_posts":
                health_posts.terminate()
            elif command == "print_date":
                os.system("date")
            elif command == "get_new_client":
                new_client_url = (BASE_URL +
                                  "/get_new_client/" +
                                  COMMON_SETTINGS['COMPANYNAME'] + '/' +
                                  COMMON_SETTINGS['HARDWARENAME'])
                os.system("curl " + new_client_url + " > new_client.py")
                logger.info("new_client.py created")
            elif command == "run_new_client":
                new_client_proc = Popen(['python', 'new_client.py'])
            elif command == "stop_new_client":
                try:
                    new_client_proc.terminate()
                except Exception:
                    logger.info("unable to terminate new_client")
            time.sleep(10)


def gateway_mgmt(config_gets, health_posts, conversion_gets):
    """Runs the manager for handling commands for the gateway

    This manages commands just for the gateway and not for any
    connected instruments, devices, etc.
    """
    gateway_manager = GatewayManager()
    gateway_manager.command_handler(config_gets, health_posts, conversion_gets)


class Nanny(object):
    """Monitors gateway client and restarts if necessary

    The Nanny uses two ways of verifying the processes.

       1) It checks if the requests processes are active by checking
          if the unix pid is active.
       2) It checks if the config gets process is still updating the
          counter file. If the file is not getting updated anymore,
          then the process is likely hung up from running a config

    In either case, if a problem is detected then the process is
    restarted and the Nanny continues monitoring
    """
    def __init__(self):
        self.config_gets_active = False
        self.health_posts_active = False

    def active_pid(self, pid):
        """ Check if active unix pid. """
        if psutil.pid_exists(pid):
            return True
        else:
            logger.info("The process with pid %s does not exist" % pid)
            return False

    def start_config_gets(self):
        config_gets_ps = multi.Process(target=config_gets)
        config_gets_ps.start()
        with open("config_gets.pid", "w") as f:
            f.write(str(config_gets_ps.pid))
        with open("config_gets.pid", "r") as f:
            config_gets_pid = int(f.read())
        self.config_gets_active = self.active_pid(config_gets_pid)

    def start_health_posts(self):
        health_posts_ps = multi.Process(target=health_posts)
        health_posts_ps.start()
        with open("health_posts.pid", "w") as f:
            f.write(str(health_posts_ps.pid))
        with open("health_posts.pid", "r") as f:
            health_posts_pid = int(f.read())
        self.health_posts_active = self.active_pid(health_posts_pid)

    def check_if_requests_active(self):
        """Check request processes, restart if not running"""
        logger.info("Nanny executing check_if_requests_active")
        try:
            with open("config_gets.pid", "r") as f:
                config_gets_pid = int(f.read())
            self.config_gets_active = self.active_pid(config_gets_pid)
        except Exception:
            self.config_gets_active = False
        if not self.config_gets_active:
            self.start_config_gets()
        try:
            with open("health_posts.pid", "r") as f:
                health_posts_pid = int(f.read())
            self.health_posts_active = self.active_pid(health_posts_pid)
        except Exception:
            self.health_posts_active = False
        if not self.health_posts_active:
            self.start_health_posts()

    def check_counter_file(self, ps1, last_update):
        """Checks if the updates to the counter file

        Verifies that config check process is still updating the
        counter file. If not, then the process is most likely hung up
        and so it is terminated and a new process is started.
        """
        logger.info("Checking counter_file")
        with open("counter_file.txt", "r") as f:
            filestr = f.read()
        if filestr == last_update:
            logger.warning("No new file update..." + filestr)
            # ps1.terminate()
            # ps1 = multi.Process(name='restartConfigChecks',
            #                     target=config_gets,)
            # ps1.start()
        else:
            logger.info(filestr)
        return ps1, filestr  # filestr becomes the new last_update

    def run(self, seconds_btw_updates=600):
        """Runs the nanny

        sec_btw_updates - the grace period between updates that the
                          nanny allows the config runner process.
                          Defaults to 600 secs (10 mins)
        """
        while True:
            logger.info("Nanny run before wait")
            try:
                self.check_if_requests_active()
            except Exception:
                SENTRY_CLIENT.captureException()
            time.sleep(seconds_btw_updates)
            logger.info("Nanny run after wait")


def run_nanny():
    """Runs nanny process to monitor client"""
    client_nanny = Nanny()
    client_nanny.run()


def start_processes():
    """Kicks off all gateway client processes"""

    logger.info("starting processes")
    nanny_process = multi.Process(target=run_nanny,
                                  name='nanny_process:' +
                                  COMMON_SETTINGS['DOMAIN'])
    nanny_process.start()


pid = str(os.getpid())
pidfile = "/tmp/mydaemon.pid"


def post_config_form(instruments=None):
    if not instruments:
        instruments = INSTRUMENTS
    # upload all config forms for available instruments
    for instrument in instruments:
        inst_name = instrument["product"]
        if inst_name in dir(schema_forms):
            FORM_DICT = getattr(schema_forms, inst_name).FORM_DICT
            SCHEMA_DICT = getattr(schema_forms, inst_name).SCHEMA_DICT
        else:
            FORM_DICT = "unavailable for instrument: "+inst_name
            SCHEMA_DICT = {}
        if "fancy_name" in instrument.keys():
            inst_fancy_name = instrument["fancy_name"]
        else:
            inst_fancy_name = inst_name
        _data = {"schema": SCHEMA_DICT, "form": FORM_DICT, "defaults": [],
                 "instrument_type": inst_fancy_name}
        schema_url = urljoin(BASE_URL, "schemaform")
        headers = gateway_helpers.get_headers()
        session = requests.session()
        response = session.post(schema_url, headers=headers,
                                data=json.dumps(_data))
        assert response.status_code == 200


class OrderProcessor(object):
    """Handles isntructions from server"""
    def __init__(self, session, setup_q):
        self.session = session
        self.setup_q = setup_q
        self.scope_q = Queue()
        self.motor_q = Queue()
        self.threads = []

    def start(self, time_btw_checks=0.1):
        """Starts order processing

        Spawns three child threads:

        1. Runs the motor client indefinitely
        2. Handles scope trace orders
        3. Handles motor orders to pass to motor client

        The while loop will check the setup queue for new
        instructions from the server. Once a setup is found
        it is passed to the appropriate child thread based
        on the type of order it is.
        """
        try:
            self.motor_client = test_runners.MotorClient(self.session)
            mct = Thread(target=self.motor_client.run, name='motor_client')
            self.threads.append(mct)
            sct = Thread(target=self.handle_scope_orders, name='scope_orders')
            self.threads.append(sct)
            mot = Thread(target=self.handle_motor_orders, name='motor_orders')
            self.threads.append(mot)
            for t in self.threads:
                t.start()
            while True:
                if not self.setup_q.empty():
                    setup = self.setup_q.get()
                    if setup['break_queue']:
                        break
                    self.direct_setup(setup)
                time.sleep(time_btw_checks)
            for t in self.threads:
                t.join()
        except Exception:
            SENTRY_CLIENT.captureException()

    def direct_setup(self, setup):
        """Directs the test setup order from the server

        Depending on the test type, the this function will
        put the order in the appropriate queue
        """
        logger.info("processing run request: %s" % setup)
        if setup['label'] == "MotorController":
            self.motor_q.put(setup)
        else:
            self.scope_q.put(setup)

    def handle_scope_orders(self, time_btw_checks=0.1):
        """Checks for scope trace orders and runs them

        When a scope trace order is found, a TestRunner
        is created and is used to run the setup
        """
        while True:
            time.sleep(time_btw_checks)
            if not self.scope_q.empty():
                setup = self.scope_q.get()
                test_runner = test_runners.TestRunner(self.session)
                test_runner.run_command(setup)

    def handle_motor_orders(self, time_btw_checks=0.1):
        """Checks for motor orders and sends them over

        When a new (changed from prev) motor order is found
        the order is sent to the motor client.
        """
        prev_order = None
        while True:
            time.sleep(time_btw_checks)
            # check if there motor order in q from server
            if not self.motor_q.empty():
                motor_order = self.motor_q.get()
                # if the motor order matches the last, skip it
                if motor_order == prev_order:
                    continue
                # try to send the order to the client
                self.send_motor_client_order(motor_order)
                prev_order = motor_order

    def send_motor_client_order(self, setup):
        """Sends the setup instructions to the motor client

        This will overwrite the setup the motor client is
        using and can interrupt instructions if needed.
        """
        config = setup['config']
        cb_log = not (setup["test_run"]["config_type"].find("_canbus") >= 0)
        if not config and cb_log:
            logger.warning("Run request missing config data. Setup is: %s"
                           % str(setup))
            raise ValueError("Run request missing config data. Setup is: %s"
                             % str(setup))
        else:
            self.motor_client.setup = setup


def run():
    # try:
    #     post_config_form()
    # except Exception:
    #     SENTRY_CLIENT.captureException()
    run_nanny()


if __name__ == "__main__":
    run()
