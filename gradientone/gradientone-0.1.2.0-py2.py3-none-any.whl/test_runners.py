#!/usr/bin/python

"""

Copyright (C) 2016-2017 GradientOne Inc. - All Rights Reserved
Unauthorized copying or distribution of this file is strictly prohibited
without the express permission of GradientOne Inc.

"""

import collections
import multiprocessing as multi
import traceback
from configparser import ConfigParser
from json import dumps
from time import sleep, time

from enum import Enum

import usb

from gradientone.device_drivers.can.CANcard import CanFrame
from gradientone.gateway_helpers import get_headers

try:
    from urllib.parse import urljoin
except:
    from urlparse import urljoin

import gateway_helpers
import tek_grl_configs
import transformers
import transmitters

from gateway_helpers import print_debug

from gradientone.device_drivers.can.can_helpers import \
    lookup_trace_variable_unit_name
from gradientone.device_drivers.can.motor import Motor, PROPERTIES
from gradientone.schema_forms.ADP05518 import TRACE_VARIABLES


cfg = ConfigParser()
cfg.read('/etc/gradient_one.cfg')
COMMON_SETTINGS = cfg['common']
CLIENT_SETTINGS = cfg['client']


SENTRY_CLIENT = gateway_helpers.get_sentry()

if COMMON_SETTINGS["DOMAIN"].find("localhost") == 0 or COMMON_SETTINGS[
    "DOMAIN"].find("127.0.0.1") == 0:
    BASE_URL = "http://" + COMMON_SETTINGS["DOMAIN"]
else:
    BASE_URL = "https://" + COMMON_SETTINGS["DOMAIN"]

CLIENT_ID = 'ORIGINAL'
SAMPLE_FILE = 'MDO30121M.txt'
CONFIG_URL = (BASE_URL, '/testplansummary/' +
              COMMON_SETTINGS['COMPANYNAME'] + '/' +
              COMMON_SETTINGS['HARDWARENAME'])
DEFAULT_TEK_TYPE = 'TektronixMDO3012'

# Careful! Setting BREATH_TIME any lower can cause issues.
# The 'instance hours' issue can happen by repeatedly
# making 100 requests per second and every second.
# HTTPS requests don't work that quickly anyway,
# so going lower than 0.25 is a waste of bandwidth
BREATH_TIME = 0.25

CANBUS_URL = urljoin(BASE_URL, "motor/canbus")

logger = gateway_helpers.logger


class MotorState(Enum):
    IDLE = 0
    HOMING = 1
    MOVING = 2


def canframe_to_dict(frame):
    command_code = frame.data[0] if len(frame.data) > 0 else None
    address = [frame.id /256, frame.id % 256]
    print("converting frame:"+str(frame.id)+" "+str(address))
    return {"address": address, "command_code": command_code,
            "frame_data": frame.data[1:], "explanation": frame.explanation,
            "written": True}


def convert_numpy_points(data_points):
    # removes numpy datatypes from data
    for i in range(len(data_points)):
        for key in data_points[i].keys():
            # purely for typing reduction
            dp = data_points[i][key]
            data_points[i][key] = dp if type(dp) == str or type(
                dp) == bool else float(dp)
    return data_points


class TestRunner(object):
    """TestRunner runs the 'test' instructions form the server

       Note that a 'test' is not always an actual pass/fail test,
       the 'test' could be a configured scope waveform trace, or
       just a powermeter reading, or instructions for a motor, etc.

       run_command - this is the top level function that gets
                       when the client code creates a test_run
       single_run - most test runs will call this for a single run
       get_trace - when a trace is needed from the instrument,
                   this uses a Transformer for the instrument
                   to pass instructions and get the trace data,
                   then returns a Transmitter to send to server
    """

    def __init__(self, session):
        super(TestRunner, self).__init__()
        self._test_run = None
        self.setup = None  # setup is being deprecated for 'command'
        self.command = None
        self.session = session
        headers = gateway_helpers.get_headers()
        self.session.headers.update(headers)

        # Timer sets and clears the timeouts
        self.timer = gateway_helpers.Timer()
        # the connection to the copley card
        self.card = None
        self.logger = logger

    @property
    def test_run(self):
        self._test_run = collections.defaultdict(str)
        if self.setup:
            self._test_run.update(self.setup)
        return self._test_run

    def run_command(self, command):
        self.command = command
        self.setup = command  # setup is being deprecated for 'command'
        label = self.setup['label']
        # update command status
        data = {
            'status': 'in progress',
            'command_id': command['id']
            }
        logger.info("Updating %s to a %s status"
                    % (command['id'], data['status']))
        resp = self.session.put(BASE_URL + '/commands', data=data)
        logger.debug("Response to updating status: %s" % resp.text)
        if label == 'GRL':
            self.run_grl_test()
        elif label == 'single_run':
            trace = self.single_run()
        elif label == 'start_repeating':
            pass
        elif label == 'stop_repeating':
            pass
        elif command['category'] == 'Capture':
            print_debug("cloud capture or autoset order received")
            trace = self.get_trace()
        elif label == 'reset_usb_device':
            tag = command['device_tag']
            if not tag:
                tag = 'Tektronix'
            gateway_helpers.reset_device_with_tag(tag)
        else:
            logger.warning("test_run with no control commands")
        if trace:
            transmit_ps = multi.Process(target=transmitters.transmit_trace,
                                        args=(trace, command, self.session),
                                        name='nanny_process:' +
                                             COMMON_SETTINGS['DOMAIN'])
            transmit_ps.start()

    def run_grl_test(self):
        grl = tek_grl_configs.Grl_Test()
        result = grl.run_grl_test()
        print_debug("grl result:" % result)

    def gen_data(self):
        test_run_id = self.setup["test_run"]["id"]
        if test_run_id == 0:
            raise ValueError("Test run id is zero! Setup is:" + str(
                self.setup))
        return {"test_run_id": test_run_id}

    def single_run(self):
        print_debug("Received single run start order", post=True)
        ses = self.session
        trace = None
        try:
            trace = self.get_trace()
        except usb.core.USBError as e:
            print_debug("USBError!", post=True, trace=True)
            gateway_helpers.handle_usb_error(ses, e)
        except Exception:
            logger.error("unexpected exception in running trace")
            logger.error(traceback.format_exc())
            SENTRY_CLIENT.captureException()
        return trace

    def _get_instrument(self):
        self.timer.set_timeout(30)
        instr = None
        try:
            print_debug("getting instrument")
            instr = gateway_helpers.get_instrument(self.command['info'])
        except usb.core.USBError:
            print_debug("USBError!", post=True, trace=True)
            # reset and retry
            gateway_helpers.reset_device_with_tag()
            sleep(1)
            instr = gateway_helpers.get_instrument(self.command['info'])
        except Exception:
            logger.warning("Failed to get instrument instance", exc_info=True)
            SENTRY_CLIENT.captureException()
        if not instr:
            logger.warning("No instrument available for trace")
            return None
        self.timer.clear_timeout()
        return instr

    def _get_transformer(self, instr=None):
        try:
            i_transformer = transformers.get_transformer(self.command, instr,
                                                         self.session)
        except Exception:
            print_debug("unable to build transformer... no trace")
            print_debug("closing intrument without receiving trace")
            if instr:
                instr.close()
            print_debug(traceback.format_exc())
            SENTRY_CLIENT.captureException()
            return None
        return i_transformer

    def get_trace(self):
        """ Gets a trace from the instrument.

            This uses a Transformer for the instrument to pass
            instructions and get the trace data, then returns a
            trace object. The trace object is an instance of
            Transmitter that transmits the trace results and test
            run related data. By default it will retry once in case
            it fails on the first try.
        """
        print_debug("get trace called")
        # obtain instrument for trace
        instr = self._get_instrument()
        if not instr:
            return
        # get transformer for instrument
        i_transformer = self._get_transformer(instr)

        # get trace from instrument by running setup with transformer
        trace = None
        try:
            print_debug("running trace setup")
            trace = self.process_transformer(i_transformer)
            print_debug("process_transformer ran with no errors")
        except KeyError:
            print_debug("KeyError exception in running setup",
                        post=True, trace=True)
            print_debug(traceback.format_exc())
            SENTRY_CLIENT.captureException()
            # no retry on key errors
        except Exception:
            print_debug("Run config failed. Unexpected error",
                        post=True, trace=True)
            SENTRY_CLIENT.captureException()
            # unexpected error, try again
            trace = self.process_transformer(i_transformer)
        finally:
            print_debug("instrument processing complete, closing connection")
            instr.close()
            return trace

    def get_initial_excerpt(self, i_transformer):
        """Returns the intial config excerpt from instrument

        It's important to call this before fetching measurements.
          1) It initializes the instrument and syncs up transformer
          2) It gets an initial state, which is good for debugging

        i_transformer: object that reads back the appropriate
                       fields for the instrument type

        """
        self.timer.set_timeout(240)
        initial_excerpt = None
        try:
            initial_excerpt = i_transformer.get_config_excerpt()
            msg = "initial config setup from instrument: %s" % initial_excerpt
            print_debug(msg, post=True)
        except usb.core.USBError as e:
            print_debug("USBError!", post=True, trace=True)
            i_transformer.handle_usb_error(e)
        except Exception:
            print_debug("exception in config_excerpt initialization",
                        post=True, trace=True)
            SENTRY_CLIENT.captureException()
        self.timer.clear_timeout()
        return initial_excerpt

    def load_config(self, i_transformer, trace_dict):
        """loads config to instrument"""
        test_run = self.test_run
        if test_run['hybrid'] or test_run['autoset']:
            print_debug("measuring without loading config")
            trace_dict['config_name'] = str(test_run['id'])
        else:
            trace_dict['config_name'] = self.config['name']
            self.timer.set_timeout(60)
            try:
                i_transformer.load_config()
            except usb.core.USBError as e:
                print_debug("USBError!", post=True, trace=True)
                i_transformer.handle_usb_error(e)
            except Exception:
                print_debug("Exception in calling load_config()", post=True)
                print_debug(traceback.format_exc(), post=True)
                SENTRY_CLIENT.captureException()
            self.timer.clear_timeout()

    def get_meas_dict(self, i_transformer):
        print_debug("initiate measurement")
        i_transformer.instr.measurement.initiate()
        self.timer.set_timeout(300)
        meas_dict = collections.defaultdict(str)
        try:
            meas_dict = i_transformer.fetch_measurements()
        except usb.core.USBError as e:
            print_debug("USBError Fetching measurments", post=True, trace=True)
            i_transformer.handle_usb_error(e)
        except Exception:
            print_debug("fetch_measurements exception")
            print_debug(traceback.format_exc())
            SENTRY_CLIENT.captureException()
        self.timer.clear_timeout()
        return meas_dict

    def get_instrument_info(self, i_transformer):
        self.timer.set_timeout(120)
        instr_info = collections.defaultdict(str)
        try:
            instr_info = i_transformer.get_instrument_info()
        except Exception:
            print_debug("fetch instrument info exception",
                        post=True, trace=True)
            SENTRY_CLIENT.captureException()
        self.timer.clear_timeout()
        return instr_info

    def get_metadata(self, i_transformer):
        metadata = collections.defaultdict(str)
        metadata.update(i_transformer.trace_dict)
        metadata['instr_info'] = self.get_instrument_info(i_transformer)
        self.timer.set_timeout(120)
        try:
            # instrument fetch_setup dump
            metadata['config_info'] = i_transformer.fetch_config_info()
            # read instrument using ivi fields
            metadata['config_excerpt'] = i_transformer.get_config_excerpt()
        except Exception:
            print_debug("post-trace fetch config exception",
                        post=True, trace=True)
            metadata['config_info'] = collections.defaultdict(str)
            metadata['config_excerpt'] = collections.defaultdict(str)
            SENTRY_CLIENT.captureException()
        self.timer.clear_timeout()
        i_transformer.times['complete'] = time()
        i_transformer.update_scorecard_times()
        return metadata

    def update_with_test_run_info(self, trace_dict, test_run):
        trace_dict['test_run_name'] = test_run['name']
        trace_dict['test_plan'] = test_run['test_plan']
        trace_dict['test_run_id'] = test_run['id']
        trace_dict['instrument_type'] = test_run['instrument_type']
        trace_dict['g1_measurement'] = test_run['g1_measurement']
        return trace_dict

    def process_transformer(self, i_transformer):
        """Runs the setup on the instrument to get trace with measurments

        Called by get_trace(), this function processes transformer to
        collect instrument data, including measurements, config, and
        other metadata. These make up a trace_dict that is passed to
        the Transmitter constructor.

            i_transformer: Transfomer object being processed. This is used
                           to build a trace_dict to then use for the
                           Transmitter contructor.

        Returns a Transmitter object to transmit the trace
        """
        test_run = self.test_run
        test_run.update(i_transformer.test_run)
        trace_dict = collections.defaultdict(str)
        ses = i_transformer.session
        # reset config if 'hybrid' flag found
        if test_run['hybrid']:
            self.config = 'hybrid'
        else:
            self.config = i_transformer.config
        print_debug("config in setup is: %s" % self.config)
        # sets the ivi usb timeout
        i_transformer.instr._interface.timeout = 25000
        # check for special grl_test
        if test_run['g1_measurement'] == 'grl_test':
            print("name = ", test_run['config_name'])
            trace_dict['config_name'] = self.config['name']
            i_transformer.start_test()
            trace_dict['meas_dict'] = collections.defaultdict(str)
        else:
            trace_dict['initial_excerpt'] = self.get_initial_excerpt(
                i_transformer)  # noqa
            self.load_config(i_transformer, trace_dict)
            trace_dict['meas_dict'] = self.get_meas_dict(i_transformer)
        # update with transformer dict
        trace_dict.update(i_transformer.trace_dict)
        # update with test_run info, with priority over transformer
        self.update_with_test_run_info(trace_dict, test_run)
        # update with the collected trace metadata
        trace_dict.update(self.get_metadata(i_transformer))
        trace_dict['i_settings'] = self.test_run
        # build transmitter to return and eventually transmit trace
        my_transmitter = transmitters.get_transmitter(
            i_transformer, trace_dict, ses)
        # if cloud capture then transmit configuration for server db storage
        if test_run['hybrid'] or test_run['autoset']:
            my_transmitter.transmit_config()

        return my_transmitter


class MotorClient(TestRunner):

    def __init__(self, session):
        super(MotorClient, self).__init__(session)
        self.session = session
        self.setup = collections.defaultdict(str)
        self.last_setup = None
        # the connection to the copley card
        self.card = None
        self.card = Motor(CLIENT_SETTINGS["CANOPEN_ADDRESS"])
        self.card.open(baud=1000000)
        self.card.clear_pdos()
        self.start_time = time()

    def get_frame(self, frame_index=-1):
        _data = self.gen_data()
        if frame_index:
            _data["frame_index"] = frame_index
        response = self.session.get(CANBUS_URL, headers=get_headers(),
                                    params=_data)
        assert response.status_code == 200
        response = response.json()
        if response == "No data found for request":
            return None
        return response

    def post_frame(self, frame):
        _data = self.gen_data()
        _data["frames"] = [canframe_to_dict(frame)]
        response = self.session.post(CANBUS_URL, headers=get_headers(),
                                     data=dumps(_data))
        assert response.status_code == 200

    def update_frame(self, new_vals, index=-1):
        _data = self.gen_data()
        if not isinstance(new_vals, dict):
            new_vals = canframe_to_dict(new_vals)
        _data.update(new_vals)
        if index == -1:
            _data["method"] = "update"
        else:
            _data["method"] = "insert"
            _data["frame_index"] = index
        _data["time"] = str(time()-self.start_time)
        response = self.session.put(CANBUS_URL, headers=get_headers(),
                                    data=dumps(_data))
        assert response.status_code == 200

    def run_motor(self):
        if self.test_run["config_type"] == "trace":
            self.run_motor_trace()
            return
        if self.test_run["config_type"] == "start_canbus":
            self.run_canbus()

    def run_canbus(self):
        self.start_time = time()
        self.card.frames_list = []
        # get all frames
        incoming_frame = self.get_frame(frame_index=None)
        if incoming_frame is None:
            # no frames received
            raise ValueError("No frames received!")
        else:
            if "frames" in incoming_frame:
                frames_to_write = incoming_frame["frames"]
            else:
                frames_to_write = [incoming_frame]
        for current_frame in range(len(frames_to_write)):
            frame_to_write = frames_to_write[current_frame]
            if frame_to_write["written"]:
                continue
            print("incoming frame index:", frame_to_write["frame_index"])
            address = (frame_to_write["address"][0] << 8) + \
                       frame_to_write["address"][1]
            if "command_code" in frame_to_write.keys():
                data = [frame_to_write["command_code"]]
            else:
                data = []
            data += frame_to_write["frame_data"]
            self.card.frames_list = []
            xmit_frame = CanFrame(id=address, data=data)
            self.card.send_ack(xmit_frame)
            frame_to_write["written"] = True
            self.update_frame(frame_to_write)
            # if there was a response, post it!
            insert_index = frame_to_write["frame_index"]+1
            for response_frame in self.card.frames_list:
                self.update_frame(response_frame,
                                  index=insert_index)
                insert_index += 1
            # update the subsequent frames
            for subsequent_frames in range(current_frame+1, len(frames_to_write)):
                frames_to_write[subsequent_frames]["frame_index"] += len(self.card.frames_list)

    def run_motor_trace(self):
        # Trace data mode
        state = MotorState.IDLE
        config_parts = ["motor_end_position", "properties", "time_window",
                        "trace"]
        self.card.clear_pdos()
        while True:
            sleep(BREATH_TIME)

            print("Motor state is: "+str(state)+ " setup is: "+str(self.setup["config"]["config_excerpt"]))
            test_order = self.setup["config"]["config_excerpt"]
            print(" got stuff: "+ str(set(config_parts).issubset(test_order.keys())))

            if state == MotorState.IDLE and \
                    not set(config_parts).issubset(test_order.keys()):
                msg = "In run motor, test order missing parts:" + str(
                    list(set(config_parts) - set(test_order.keys())))
                logger.error(msg)
                raise ValueError(msg)
            elif state == MotorState.IDLE:
                print("initializing poll variables")
                test_order["properties"] = [str(prop) for prop in
                                            test_order["properties"]]
                # set up parameters once
                if test_order["trace"] == "poll":
                    for parameter in test_order["properties"]:
                        _ = self.card.property_getter(parameter)
                print("setting to homing")
                state = MotorState.HOMING
            if self.card.unplugged:
                return
            if state == MotorState.HOMING:
                self.card.move(0)
                if self.card.property_getter("actual_position") == 0:
                    self.card.start_time = time()
                    state = MotorState.MOVING
            elif state == MotorState.MOVING:
                self.card.move(test_order["motor_end_position"])
                print("doing trace")
                data_points = self.card.do_trace(max_counts=10000,
                                                 max_time=test_order[
                                                     "time_window"],
                                                 properties=test_order[
                                                     "properties"],
                                                 sync=test_order[
                                                          "trace"] == "poll")
                # update the test to complete, then return to idle
                _data = self.gen_data()
                data_points = convert_numpy_points(data_points)
                _data["data"] = data_points
                _data["units"] = {}
                for key in data_points[0].keys():
                    if key in PROPERTIES.keys():
                        _data["units"][key] = PROPERTIES[key]["units"]
                    elif key in TRACE_VARIABLES:
                        _data["units"][key] = lookup_trace_variable_unit_name(
                            key)
                response = self.session.post(urljoin(BASE_URL, "/motor/data"),
                                             headers=get_headers(),
                                             data=dumps(_data))
                assert response.status_code == 200
                logger.info("Done motor trace")
                return

    def run(self):
        while True:
            try:
                # this check for whether the setup is the same as the last
                # is required, or the client will do the same trace over and
                #  over again.
                if self.last_setup != self.setup:
                    self.run_motor()
                    self.last_setup = self.setup
            except Exception:
                SENTRY_CLIENT.captureException()
            sleep(1)
