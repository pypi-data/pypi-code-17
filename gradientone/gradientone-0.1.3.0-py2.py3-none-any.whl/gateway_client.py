"""

Copyright (C) 2016-2017 GradientOne Inc. - All Rights Reserved
Unauthorized copying or distribution of this file is strictly prohibited
without the express permission of GradientOne Inc.

"""

import collections
import datetime
import json
import os
from Queue import Queue
from subprocess import Popen, PIPE

from gradientone.test_runners import MotorClient

try:
    from urllib.parse import urljoin
except:
    from urlparse import urljoin

import time
import traceback
from configparser import ConfigParser
import requests
import gateway_helpers
import misc_scope
import tek_grl_configs
import test_runners
from device_drivers import usb_controller
from controllers import ClientInfo, MultiClientController

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
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DIRPATH = os.path.dirname(os.path.realpath(__file__))


class ScopeClient(object):
    """Manages config related client workflow"""
    def __init__(self):
        self.session = requests.session()
        self.setup_q = Queue()

    """Manages configs for instruments from the server"""
    def check_config_url(self):
        """polls the configuration URL for a test run object"""
        config_url = CONFIG_URL
        headers = gateway_helpers.get_headers()
        params = {'status': 'pending', 'tag': "Scope"}
        response = self.session.get(config_url, headers=headers, params=params)
        if response.status_code != 200:
            raise ValueError("bad status: "+str(response.status_code) +
                             " on url: "+str(config_url))
        if response.status_code == 401:
            headers = gateway_helpers.get_headers(refresh=True)
            response = self.session.get(config_url, headers=headers)
        if response:
            # only process response if there are commands
            if len(response.json()["commands"]) > 0:
                logger.info("Processing response: "+str(response.text) +
                            " config_url "+str(config_url))
                self.process_response(response)
        else:
            logger.error("No response from server")

    def check_for_configs(self, client_info):
        logger.info("Starting checks for configs")
        while True:
            logger.info("ScopeClient is alive")
            try:
                self.check_config_url()
            except Exception:
                logger.warning("check_config_url exception", exc_info=True)
                SENTRY_CLIENT.captureException()
            time.sleep(1)
            update_activity_file(client_info.activity_file)

    def process_response(self, response):
        """Processes response from server to config get requests

        Checks if command is a Config or Capture before running.

        Else checks if it's 'check_scope'
        Else checks if it's some other Special command
        Else it considers the response a no command
        """
        if not response.text:
            logger.debug("No response text")
            return
        try:
            commands = json.loads(response.text)['commands']
            if commands:
                command = collections.defaultdict(str, commands[0])
            else:
                command = None
        except Exception as e:
            logger.warning("Exception loading setup data, e:%s reponse is:%s"
                           % (e, response.text))
            return
        if not command:
            logger.debug("No command; Time:" + str(datetime.datetime.now()) +
                         "; Gateway:" + COMMON_SETTINGS['HARDWARENAME'] +
                         "; Company:" + COMMON_SETTINGS['COMPANYNAME'] +
                         "; Domain:" + COMMON_SETTINGS['DOMAIN'])
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
        else:
            logger.info("Unexpected command in response: %s" % command)

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


def update_activity_file(activity_file):
    """Updates counter for nanny to check"""
    with open(activity_file, 'w') as f:
        f.write(datetime.datetime.now().strftime(DATETIME_FORMAT))


def scope_client(client_info):
    """Starts the manager for getting and running configs"""
    logger.info("initializing ScopeClient in scope_client")
    cfg_manager = ScopeClient()
    cfg_manager.check_for_configs(client_info)
    # cfg_manager.start_threads()  # for multi-threaded command processing


def motor_client(client_info):
    """Starts the manager for getting and running configs"""
    with open("motor_client.pid", 'w') as f:
        f.write(str(os.getpid()))
    logger.info("initializing MotorClient in motor_client")
    cfg_manager = MotorClient()
    cfg_manager.run()


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
            "company": COMMON_SETTINGS["COMPANYNAME"],
        }
        data = json.dumps(payload)
        logger.debug("Posting to: %s with data: %s" % (health_url, data))
        self.session.post(health_url, data=data)
        # migrate towards using the following in place of /gateway/health
        url = BASE_URL + '/gateway'
        payload = {
            "name": COMMON_SETTINGS['HARDWARENAME'],
            "company": COMMON_SETTINGS['COMPANYNAME'],
            "client_version": self.get_client_version(),
        }
        data = json.dumps(payload)
        self.session.post(url, data=data)

    def run(self, client_info):
        """Runs the health manager indefinitely"""
        while True:
            logger.info("HealthManager is alive")
            try:
                self.post_health_data()
                update_activity_file(client_info.activity_file)
            except Exception:
                logger.info("post health data exception", exc_info=True)
                SENTRY_CLIENT.captureException()
            time.sleep(SECONDS_BTW_HEALTH_POSTS)

    def get_client_version(self, package='gradientone'):
        """Gets version by parsing pip output"""
        pip_show_pkg = ['pip', 'show', package]
        output = Popen(pip_show_pkg, stdout=PIPE).communicate()[0]
        lines = output.split('\n')
        version = ""
        for line in lines:
            if line.startswith("Version:"):
                version = line.split(':')[1].strip()
        return version


def health_posts(client_info):
    """Runs the manager that posts gateway health info"""
    with open("health_posts.pid", 'w') as f:
        f.write(str(os.getpid()))
    health_manager = HealthManager()
    health_manager.run(client_info)


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


class GatewayClient(MultiClientController):

    def __init__(self, *args, **kwargs):
        super(GatewayClient, self).__init__(*args, **kwargs)

        """Gathers the client infos to kickoff with controller

        The targets and names are used to create ClientInfo objects used in
        the MultiClientController kickoff() method. The keep_alive_interval
        is the seconds allowed to pass between updates to the activity file
        before the controller will restart the client process.

        Note that the MultiClientController will pass the ClientInfo object
        to the target function so that the function will have the client
        info, most importantly the activity_file that it needs to update
        periodically within the keep_alive_interval
        """
        file = os.path.join(DIRPATH, 'scope_client_activity.txt')
        scope_info = ClientInfo(target=scope_client, name='scope_client',
                                keep_alive_interval=1200, activity_file=file)
        file = os.path.join(DIRPATH, 'health_posts_activity.txt')
        hposts_info = ClientInfo(target=health_posts, name='health_posts',
                                 keep_alive_interval=120, activity_file=file)
        file = os.path.join(DIRPATH, 'motor_posts_activity.txt')
        motor_info = ClientInfo(target=motor_client, name='motor_client',
                                keep_alive_interval=120, activity_file=file)
        client_infos = [scope_info, hposts_info, motor_info]

        # Other clients to be kickoff by the MultiClientController should
        # be added here. Be sure to create a ClientInfo object with
        # the appropriate target, name, keep_alive_interval, and
        # activity file. Then append the object to client_infos

        for client_info in client_infos:
            self.clients_dict[client_info.name] = client_info
