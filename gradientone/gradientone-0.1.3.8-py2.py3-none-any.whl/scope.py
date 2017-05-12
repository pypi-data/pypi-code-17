"""

Copyright (C) 2016-2017 GradientOne Inc. - All Rights Reserved
Unauthorized copying or distribution of this file is strictly prohibited
without the express permission of GradientOne Inc.

"""

import collections
import datetime
import json
import numpy as np
import traceback
import time
import usb

import gateway_helpers as helpers
import tek_grl_configs
import test_runners
from configparser import ConfigParser
from device_drivers import usb_controller
from base import BaseClient


# Read in config file info
cfg = ConfigParser()
PATH_TO_CFG_FILE = '/etc/gradient_one.cfg'
cfg.read(PATH_TO_CFG_FILE)
COMMON_SETTINGS = cfg['common']
CLIENT_SETTINGS = cfg['client']
DEFAULT_TEK_TYPE = 'TektronixMDO3012'
BASE_URL = helpers.BASE_URL
MAX_VALID_MEAS_VAL = 1e36

# Get Sentry client for Sentry logging
SENTRY_CLIENT = helpers.get_sentry()

# For Non-Sentry logging
logger = helpers.logger


class ScopeClient(BaseClient):
    """Manages scope config related client workflow"""
    def __init__(self, *args, **kwargs):
        super(ScopeClient, self).__init__(*args, **kwargs)
        self.post_config_form([{
                "manufacturer": "Tektronix",
                "product": "TektronixMDO3012",
                "fancy_name": "TektronixMDO3012"
            },
            {
                "manufacturer": "Rigol",
                "product": "RigolMSO2302A",
                "fancy_name": "RigolMSO2302A"
            }])
        url = BASE_URL + "/gateway"
        payload = {
            "name": COMMON_SETTINGS['HARDWARENAME'],
            "company": COMMON_SETTINGS['COMPANYNAME'],
        }
        data = json.dumps(payload)
        self.put(url, data=data)
        self.dec_factor = 1

    def process_response(self, response):
        """Processes response from server to config get requests

        This gets called when check_for_commands() and
        check_command_url() get a response from the server.

        if command == Config or Capture executing w/ TestRunner()
        elif it's 'check_scope'
        elif it's some other Special command
        else it considers the response a non-command

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
            test_runner = test_runners.TestRunner(self.session)
            test_runner.run_command(command)
        # most commands will be test runs like above
        # special commands and continue commands below
        elif command['arg'] == 'check_scope':
            scope_info = None
            try:
                instrument_type = command['instrument_type']
                scope_info = self.check_scope(instrument_type)
            except Exception:
                logger.error(traceback.format_exc())
                SENTRY_CLIENT.captureException()
            finally:
                self.update_gateway_state(scope_info)
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
            self.check_or_reset(self.session, spc, setup[
                'instrument_type'])
        elif spc == 'reset_usb':
            helpers.reset_device_with_tag()
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
            self.update_gateway_state(self.session, {'grl_test': resp})
        else:
            logger.warning("unknown special command: %s" % command)
            self.update_gateway_state(self.session, {'unknown_command': spc})

    def reset_scope(self, instrument_type=DEFAULT_TEK_TYPE):
        """Calls utility.reset() to reset scope"""
        try:
            instr = helpers.get_instrument({
                'instrument_type': instrument_type})
        except Exception:
            logger.debug(traceback.format_exc())
        try:
            instr.utility.reset()
            logger.debug("instrument reset")
        except Exception:
            logger.debug(traceback.format_exc())
        finally:
            instr.close()

    def check_scope(self, instrument_type=DEFAULT_TEK_TYPE):
        """Checks acquisition type to check if scope working"""
        acq_type = None
        try:
            instr = helpers.get_instrument({
                'instrument_type': instrument_type})
        except Exception:
            logger.info(traceback.format_exc())
            return None
        try:
            acq_type = instr.acquisition.type
            acq_time_per_record = instr.acquisition.time_per_record
            trigger_type = instr.trigger.type
            trigger_coupling = instr.trigger.coupling
            logger.info("acq_type: " + acq_type)
            inst_info = {
                'acq_type': acq_type,
                'acq_time_per_record': acq_time_per_record,
                'trigger_type': trigger_type,
                'trigger_coupling': trigger_coupling,
            }
            logger.info("basic instrument info: %s" % inst_info)
            return acq_type
        except Exception:
            logger.info(traceback.format_exc())
        finally:
            instr.close()
            return acq_type

    def set_scope(self, scope_info=None):
        """Sets basic scope info to test scope"""
        scope_dict = collections.defaultdict(int)
        scope_dict.update(scope_info)
        if not scope_dict['instrument_type']:
            scope_dict['instrument_type'] = DEFAULT_TEK_TYPE
        try:
            instr = helpers.get_instrument(scope_dict)
        except Exception:
            logger.info(traceback.format_exc())
            return None
        try:
            instr.acquisition.type = scope_dict['acq_type']
            instr.acquisition.time_per_record = scope_dict['acq_time_per_record']  # noqa
            instr.trigger.type = scope_dict['trigger_type']
            instr.trigger.coupling = scope_dict['coupling']
            return True
        except Exception:
            logger.info(traceback.format_exc())
            return None

    def check_or_reset(self, session, command, instrument_type):
        """Runs ad hoc check or reset scope commands"""
        command_funcs = {
            'reset': self.reset_scope,
            'check': self.check_scope,
        }
        try:
            scope_info = command_funcs[command](instrument_type)
        except Exception:
            logger.error(traceback.format_exc())
            scope_info = None
        finally:
            self.update_gateway_state(session, scope_info)

    def _shrink(self, voltage_list, mode='normal',
                max_length=CLIENT_SETTINGS['MAX_LENGTH_FOR_BROWSER']):
        """Shinks a voltage list to a decimated waveform

        Decimated waveform needed for faster data transfer and to save
        browser memory when drawing the summary view.
        """
        logger.debug("shrinking voltage_list")
        if not self.time_step:
            logger.warning("No time_step! Cannot shrink list!")
            return voltage_list
        len_voltage_list = len(voltage_list)
        self.dec_factor = len_voltage_list / int(max_length)
        self.dec_time_step = self.dec_factor * self.time_step
        shrunk_list = [voltage_list[0]]
        index = int(self.dec_factor)

        while index < len_voltage_list:
            if mode == 'normal':
                shrunk_list.append(voltage_list[index])
                index += int(self.dec_factor)
            elif mode == 'average':
                index += int(self.dec_factor)
                mean_value = np.mean(
                    voltage_list[index - int(self.dec_factor): index])
                shrunk_list.append(mean_value)
            elif mode == 'downsample':
                # use scipy.signal.downsample
                pass
            elif mode == 'voltage_peak_to_peak':
                self.dec_factor = self.dec_factor * 2
        return shrunk_list

    def _post_summary_waveform(self):
        """Sends max dataset for full waveform views"""
        test_run_id = self.test_run_id
        url_d = BASE_URL + "/results/" + str(test_run_id) + "/decimated"
        v_dict = {}
        for ch in self.enabled_list:
            voltage_list = self.trace_dict[ch + '_voltages']  # set in _fetch_waveform  # nopep8
            if not voltage_list:
                voltage_list = []
            if len(voltage_list) > int(CLIENT_SETTINGS['MAX_LENGTH_FOR_BROWSER']):  # nopep8
                v_dict[ch] = self._shrink(voltage_list)
            else:
                v_dict[ch] = voltage_list
        self.summary_voltages = v_dict
        if not self.dec_factor:
            self.dec_factor = 1

        payload = {
            'time_step': self.time_step,
            'dec_factor': self.dec_factor,
            'test_results': self.summary_voltages,
        }
        json_data = json.dumps(payload)
        logger.info("posting end to end waveform")
        self.post(url_d, data=json_data)
        summary_file = '/tmp/summary-waveform-%s.json' % self.test_run_id
        logger.info("Writing waveform to %s" % summary_file)
        with open(summary_file, 'w') as f:
            f.write(json_data)


class IviScopeClient(ScopeClient):
    """Manages ivi scope related client workflow"""
    def _fetch_waveform_measurements(self, ch_str, meas_dict):
        self.check_commands_completed()
        logger.debug("fetching waveform measurements")
        if not self.channels:
            channel = self.instr.channels[ch_str]
        else:
            channel = self.channels[ch_str]
        meas_dict[ch_str]['valid'] = True
        for meas in self.meas_list:

            if cfg.getboolean('client', 'SIMULATED'):
                meas_dict[ch_str][str(meas)] = "Simulated m_val"
                continue

            m_val = ''
            measurement = channel.measurement
            try:
                m_val = measurement.fetch_waveform_measurement(meas)
                self.check_commands_completed()
                meas_dict[ch_str][str(meas)] = m_val
                if m_val > MAX_VALID_MEAS_VAL:
                    meas_dict[ch_str]['valid'] = False
            except Exception:
                logger.debug(ch_str + " measurement exception")
                logger.debug(traceback.format_exc())

    def fetch_raw_setup(self, last_try=False):
        if cfg.getboolean('client', 'SIMULATED'):
            return "simulated config info"
        logger.debug("fetching raw_setup")
        try:
            raw_setup = self.instr.system.fetch_setup()
        except Exception:
            self.logger.warning("fetch setup failed", exc_info=True)
            if last_try:
                return None
            else:
                raw_setup = self.fetch_raw_setup(last_try=True)
        return raw_setup

    def load_raw_setup(self, try_count=0):
        logger.debug("loading hybrid_config")
        ascii_config = self.config['hybrid_config'].encode('ascii')
        try:
            self.instr.system.load_setup(ascii_config)
        except Exception:
            self.logger.warning("failed loading hybrid config", exc_info=True)
            if try_count > 10:
                logger.debug("not retrying")
            else:
                self.instr.close()
                time.sleep(1)
                logger.debug("retrying...")
                try_count = try_count + 1
                self.instr = helpers.get_instrument(self.test_run)
                self.load_raw_setup(try_count)

    def _setinstr(self, ivi_obj, key, value, label=''):
        try:
            setattr(ivi_obj, key, value)
            self.config_scorecard['success'].append(label + key)
            return True
        except Exception:
            logger.debug("failed setting %s" % label + key)
            logger.debug(traceback.format_exc())
            self.exception_count += 1
            self.config_scorecard['failure'].append(label + key)
            return False

    def _setinstr_with_tries(self, ivi_obj, key, value, label='', tries=3):
        success = False
        for attempt in range(tries):
            try:
                setattr(ivi_obj, key, value)
                success = True
                break
            except usb.core.USBError as e:
                logger.debug("USB Error in setting instrument", trace=True)
                self.handle_usb_error(e)
            except Exception:
                logger.debug("failed to set timebase: %s %s" %
                             (key, value), trace=True)
                self.exception_count += 1
                time.sleep(0.1)
        if success:
            self.config_scorecard['success'].append(label + key)
        else:
            self.config_scorecard['failure'].append(label + key)
