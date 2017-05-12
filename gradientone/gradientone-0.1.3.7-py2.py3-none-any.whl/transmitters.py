#!/usr/bin/python

"""

Copyright (C) 2016-2017 GradientOne Inc. - All Rights Reserved
Unauthorized copying or distribution of this file is strictly prohibited
without the express permission of GradientOne Inc.

"""


import collections
import csv
import gzip
import json
import os
import requests
import traceback
import zlib
from configparser import ConfigParser
from datetime import datetime
from requests_toolbelt.multipart.encoder import MultipartEncoder

import gateway_helpers
from gateway_helpers import logger, get_headers
from base import BaseClient
from scope import ScopeClient


cfg = ConfigParser()
cfg.read('/etc/gradient_one.cfg')
COMMON_SETTINGS = cfg['common']
CLIENT_SETTINGS = cfg['client']

SENTRY_CLIENT = gateway_helpers.get_sentry()

CLIENT_ID = 'ORIGINAL'
SAMPLE_FILE = 'MDO30121M.txt'
MAX_VALID_MEAS_VAL = 1e36

if COMMON_SETTINGS["DOMAIN"].find("localhost") == 0 or COMMON_SETTINGS["DOMAIN"].find("127.0.0.1") == 0:  # noqa
    BASE_URL = "http://" + COMMON_SETTINGS["DOMAIN"]
else:
    BASE_URL = "https://" + COMMON_SETTINGS["DOMAIN"]

CONFIG_URL = (BASE_URL + "/testplansummary/" +
              COMMON_SETTINGS['COMPANYNAME'] + '/' +
              COMMON_SETTINGS['HARDWARENAME'])


class Transmitter(BaseClient):
    # Transmits trace data received from instrument up to the server

    def __init__(self, command_id="unknown_id"):
        self.session = requests.session()
        self.session.headers.update(gateway_helpers.get_headers())
        self.trace_dict = {
            "test_run_id": command_id,
            "command_id": command_id,
        }
        self.test_run_id = command_id
        self.command_id = command_id
        self.results_dict = collections.defaultdict(str)
        self.dec_factor = 1
        self.upload_polling_metadata = True

    def format_csv(self):
        pass

    def post_result(self):
        pass

    def generate_results_dict(self):
        self.results_dict['config_name'] = "unknown"

    def post_wrapper(self, url, data="", headers={}):
        """
        This is a wrapper function to the sessions.post function to capture
        errors in the log.
        :param url: the url that the post is going to
        :param data: the data. Should be a string, if it is a dict it will be
        serialized to JSON
        :param headers: the headers. If empty, will be set to the default
        value in get_headers
        """
        if not headers:
            headers = gateway_helpers.get_headers()
        if isinstance(data, dict):
            data = json.dumps(data)
        response = self.post(url, data=data, headers=headers)
        print 'response is ', response
        assert response.status_code == 200
        logger.debug(url + " response.reason= %s" % response.reason)
        logger.debug(url + " response.status_code=%s" % response.status_code)
        return response

    def test_complete(self):
        """transmit test complete function sends a json object that is used
           to update DB on test status. Primarily metadata and indexing.
           No waveforms are sent here.
        """
        logger.info("Posting results")
        self.transmit_result_blob()
        self.generate_results_dict()
        data = json.dumps(self.results_dict)
        if self.results_dict['config_name'] == 'I2C':
            # trigger the appropriate analysis handler
            _response = self.get(BASE_URL + "/analysis",
                                 params={"test_run_id": self.test_run_id,
                                         "suite": "skywave"})
            expected_result = "[\"/markers?test_run_id=" + str(
                self.test_run_id) + "\", \"/results/" + str(
                self.test_run_id) + "/metadata\"]"
            assert _response.status_code == 200
            assert _response.text == expected_result
        if self.upload_polling_metadata:
            polling_metadata_url = (BASE_URL + "/polling/results/metadata/" +
                                    str(self.test_run_id))
            self.post(polling_metadata_url, data=data)
        data = {'command_id': self.test_run_id, 'status': 'complete'}
        commands_url = BASE_URL + "/commands"
        response = self.put(commands_url, data=json.dumps(data),
                            headers=get_headers())
        assert response.status_code == 200
        self.post_result()

    def transmit_result_blob(self, infile=''):
        """Sends test results to the blobstore

        End to end waveforms are sent here.
        """
        if not infile:
            infile = '/tmp/full-trace-%s.json' % self.test_run_id
        logger.debug("transmitting blob")
        gzip_file = infile + '.gz'
        config_name = self.trace_dict['config_name']
        with open(infile) as f_in, gzip.open(gzip_file, 'wb') as f_out:
            f_out.writelines(f_in)
        data_type = 'application/x-gzip'

        blobfile = str(config_name) + ':' + str(self.trace_dict['test_run_id'])
        multipartblob = MultipartEncoder(
            fields={
                'file': (blobfile, open(gzip_file, 'rb'), data_type),
                'test_run_id': str(self.trace_dict['test_run_id']),
                'file_key': gzip_file.split('/')[-1],
            }
        )
        blob_url = self.get(BASE_URL + "/upload/geturl")
        response = self.post(
            blob_url.text,
            data=multipartblob,
            headers={
                'Content-Type': multipartblob.content_type
            })
        self.blob_key = response.text

    def transmit_trace(self):
        """results transmission for generic instruments"""
        self.session = requests.session()
        self.session.headers.update(gateway_helpers.get_headers())
        try:
            logger.debug("transmitting trace")
            # complete transmission indexing blobstore data
            self.test_complete()
        except Exception:
            logger.error("Exception occurred during trace transmission")
            logger.error(traceback.format_exc())
            SENTRY_CLIENT.captureException()
        finally:
            tid = self.trace_dict['test_run_id']
            gateway_helpers.post_logfile(test_run_id=tid)


class CANOpenTransmitter(Transmitter):
    """
    Transmits data for CANOpen devices
    """

    def __init__(self, data=None, units=None,
                 config={"arg": "unknown_config", "id": "test-id"}):

        Transmitter.__init__(self)
        # the data is a list of dictionaries, where each key is a column
        # header, and the value with that key is the row value at that column,
        # i.e., [{'y': 0, 'x1': 9.9, 'x2': 3.2},
        #        {'y': 1, 'x1': 9.8, 'x2': 3.1},]
        self.data = data
        # the units is a dictionary with the unit names of each column in the
        # data, i.e., {'y': 's', 'x1': 'm', 'x2': 'km'}
        self.units = units
        self.config = config
        if "id" in config.keys():
            self.test_run_id = config["id"]
        # do not upload any metadata
        self.upload_polling_metadata = False

    def generate_results_dict(self):
        if self.config is not None:
            self.results_dict["config_name"] = self.config["arg"]
        else:
            self.results_dict["config_name"] = "unknown"
        self.results_dict["hardware_name"] = COMMON_SETTINGS['HARDWARENAME']
        self.results_dict["company_nickname"] = COMMON_SETTINGS['COMPANYNAME']
        self.results_dict["instrument_type"] = "Motor"
        self.results_dict["test_run_id"] = self.test_run_id
        self.results_dict["more_metadata"] = {"units": self.units}

    def format_csv(self):
        fileblob = open('tempfile.csv', 'w')
        cwriter = csv.writer(fileblob)
        column_titles = self.data[0].keys()
        cwriter.writerow(column_titles)
        for entry in self.data:
            row = [entry[key] for key in column_titles]
            cwriter.writerow(row)
        fileblob.close()

    def post_result(self):
        PAYLOAD = {
            "fields": [{
                "name": "config_name",
                "value": self.results_dict["config_name"],
                "type": "text"
            },
                {
                    "name": "hardware_name",
                    "value": self.results_dict["hardware_name"],
                    "type": "text"
                },
                {
                    "name": "instrument_type",
                    "value": self.results_dict["instrument_type"],
                    "type": "text"
                },
                {
                    "name": "test_run_id",
                    "value": self.results_dict["test_run_id"],
                    "type": "text"
                },
                {
                    "name": "parameters",
                    "value": ", ".join(self.config["info"]["config_excerpt"]["properties"]),  # noqa
                    "type": "text"
                },
                {
                    "name": "start_datetime",
                    "value": str(datetime.now()),
                    "type": "text"
                }
            ],
            "index_name": "results"
        }

        url = BASE_URL + "/search"
        self.post(url, data=json.dumps(PAYLOAD))


class ScopeTransmitter(Transmitter, ScopeClient):
    """transmits data to server for scope information"""

    def __init__(self, transformer=None, trace_data=None, session=None):
        Transmitter.__init__(self)
        self.test_run = collections.defaultdict(int)
        if transformer:
            self.test_run.update(transformer.test_run)
            self.test_run_id = self.test_run['id']
            self.command_id = self.test_run['id']
            self.time_step = transformer.time_step
            # the transformer ce_dict holds initial instructions
            self.ce_dict = transformer.ce_dict
            self.config_scorecard = transformer.config_scorecard
            self.g1_measurement_results = transformer.g1_measurement_results
            summary_file = '/tmp/summary-waveform-%s.json' % self.test_run_id
            with open(summary_file, 'r') as f:
                self.summary_voltages = f.read()
                try:
                    self.summary_voltages = json.loads(self.summary_voltages)
                except Exception as e:
                    logger.warning(e, exc_info=True)
        else:
            self.ce_dict = {}
            self.time_step = 1.0
        self.trace_dict = collections.defaultdict(int)
        if trace_data:
            self.trace_dict.update(trace_data)

        self.blob_key = None
        self.raw_data_url = (
            BASE_URL + "/results/%s.json" % self.trace_dict['test_run_id']
        )

        # this is updated with the reported config_excerpt
        if "config_excerpt" in self.trace_dict.keys():
            self.ce_dict.update(self.trace_dict['config_excerpt'])
        self.config_scorecard = transformer.config_scorecard
        self.more_metadata = collections.defaultdict(str)

        if cfg.getboolean('client', 'SIMULATED'):
            self.ce_dict['enabled_list'] = ['ch1']
        # get the default channel
        self.results_dict = {
            'test_run_id': self.trace_dict['test_run_id'],
            'channel_headers': self.ce_dict['enabled_list'],
            'test_results': transformer.first_slice,
            'hardware_name': COMMON_SETTINGS['HARDWARENAME'],
            'company_nickname': COMMON_SETTINGS['COMPANYNAME'],
            'raw_data_url': self.raw_data_url,
            'start_tse': int(self.trace_dict['start_tse']),
            'test_plan': self.trace_dict['test_plan'],
            'config_name': self.trace_dict['config_name'],
            'record_length': self.trace_dict['record_length'],
            'time_per_record': self.ce_dict['acquisition']['time_per_record'],
            'time_step': self.time_step,
            # for the new Result model, we'd just need the following
            'command_id': '',
            'config': self.trace_dict['config_name'],
            'instrument_type': self.trace_dict['instrument_type'],
            'category': '',
            'tags': [],
            'plan': '',
            'dut': '',
            # 'info': {'metadata': {}},  # everything else should migrate
        }
        self.dec_factor = 1
        self.slices = []

    def format_csv(self):
        fileblob = open('tempfile.csv', 'w')
        cwriter = csv.writer(fileblob)
        cwriter.writerow(self.ce_dict['enabled_list'])
        voltage_lists = []
        if not self.summary_voltages:
            fileblob.close()
            return
        for ch in self.summary_voltages:
            voltage_lists.append(self.summary_voltages[ch])
        for row in zip(*voltage_lists):
            cwriter.writerow(row)
        fileblob.close()

    def generate_results_dict(self):
        chart_url = 'https://' + \
            COMMON_SETTINGS['DOMAIN'] + '/result/' + str(self.test_run_id)
        screenshot_url = ('https://' + COMMON_SETTINGS['DOMAIN'] +
                          '/view_report_file/' +
                          str(self.trace_dict['screenshot_blob_key']))
        self.trace_dict['instr_info']['scope_screenshot_url'] = screenshot_url
        self.results_dict.update(self.trace_dict['instr_info'])
        extra_data = {
            'blob_key': self.blob_key,
            'results_link': chart_url,
            'test_results': self.raw_data_url,
            'raw_setup': self.trace_dict['raw_setup'],
            'config_excerpt': self.trace_dict['config_excerpt'],
            'measurements': self.trace_dict['meas_dict'],
            'more_options': self.trace_dict['more_options'],
            'g1_measurement': self.trace_dict['g1_measurement'],
            'dec_factor': self.dec_factor,
            'config_scorecard': self.config_scorecard,
            'more_metadata': self.more_metadata,
            'g1_measurement_results': self.g1_measurement_results,
            'company_nickname': COMMON_SETTINGS['COMPANYNAME'],
            'instrument_type': self.trace_dict['instrument_type'],
        }
        self.results_dict.update(extra_data)

    def transmit_file(self, filename, content_type='application/x-gzip'):
        """transmits file to blobstore

        - assumes the file is already gzipped
        - deletes the local file after successfully transmitting
        """
        test_run_id = str(self.trace_dict['test_run_id'])
        if not filename:
            filename = test_run_id + "-file.gz"
        multipartblob = MultipartEncoder(
            fields={
                'file': (filename, open(filename, 'rb'), content_type),
                'test_run_id': test_run_id,
                'file_key': filename,
            }
        )
        resp = self.get(BASE_URL + "/upload/geturl")
        headers = {'Content-Type': multipartblob.content_type}
        response = self.post(resp.text, data=multipartblob,
                             headers=headers)
        if response.status_code == 200:
            logger.info("File upload for %s succeeded!" % filename)
            os.remove(filename)
        else:
            logger.info("File upload for %s failed" % filename)

    def transmit_slice_blobs(self):
        for idx, slice_data in enumerate(self.slices):
            filename = self.command_id + '-slice-' + str(idx) + '.json.gz'
            with gzip.open(filename, 'wb') as f:
                f.write(json.dumps(slice_data))
            self.transmit_file(filename=filename)

    def transmit_slices(self):
        # post slices
        slice_url = BASE_URL + '/results/' + self.test_run_id + '/slices'
        voltage_start_time = 0
        dict_of_slice_lists = collections.defaultdict(int)
        list_of_slices = []
        for ch in self.ce_dict['enabled_list']:
            voltages = self.trace_dict[ch + '_voltages']
            # create list of slices
            list_of_slices = [voltages[x:x + int(CLIENT_SETTINGS['MAX_LENGTH_FOR_BROWSER'])]  # nopep8
                              for x in range(0, len(voltages), int(CLIENT_SETTINGS['MAX_LENGTH_FOR_BROWSER']))]  # nopep8
            dict_of_slice_lists[ch] = list_of_slices
            logger.debug("length of list of slices for %s: %s"
                         % (ch, len(list_of_slices)))
            self.more_metadata['total_points'] = len(voltages)
        for idx, slice_points in enumerate(list_of_slices):
            slices_by_channel = {}
            for ch in dict_of_slice_lists:
                if idx + 1 > len(dict_of_slice_lists[ch]):
                    logger.debug("""Warning! Slice index greater than length of
                        list of slices for %s""" % ch)
                else:
                    slices_by_channel[ch] = dict_of_slice_lists[ch][idx]
            voltage_start_time += self.time_step * len(slice_points)
            slice_data = {
                'test_run_id': self.trace_dict['test_run_id'],
                'command_id': self.trace_dict['command_id'],
                'slice_index': idx,
                'num_of_slices': len(list_of_slices),
                'voltage_start_time': voltage_start_time,
                'time_step': self.time_step,
                'test_results': slices_by_channel,
            }
            self.slices.append(slice_data)
            slice_data = zlib.compress(json.dumps(slice_data))
            headers = {'Content-Encoding': 'gzip'}
            self.post(slice_url, data=slice_data, headers=headers)
        self.more_metadata['num_of_slices'] = len(list_of_slices)
        self.more_metadata['slice_length'] = int(CLIENT_SETTINGS['MAX_LENGTH_FOR_BROWSER'])  # nopep8

    def transmit_config(self):
        """Posts config to server for storage"""
        payload = {
            'config_excerpt': self.trace_dict['config_excerpt'],
            'config_data': {
                'new_config_name': self.trace_dict['test_run_id'],
                'hybrid_config': self.trace_dict['raw_setup'],
                'instrument_type': self.trace_dict['instrument_type'],
                'company_nickname': COMMON_SETTINGS['COMPANYNAME'],
            }
        }
        create_config_url = "https://" + \
            COMMON_SETTINGS['DOMAIN'] + "/create_config"
        _response = self.post(
            url=create_config_url,
            data=json.dumps(payload),
            headers=get_headers())
        assert _response.status_code == 200

    def transmit_logs(self, to_blob=False):
        filename = str(self.test_run_id) + '.log'
        if to_blob:
            # TODO: add functionality
            # transmit_logs(test_run_id=self.test_run_id)
            return
        # else it will just go to memcache
        multipartblob = MultipartEncoder(
            fields={
                'logfile': (filename, open('client.log', 'rb'), 'text/plain'),
                'testrunid': str(self.test_run_id),
            }
        )
        log_url = "https://" + \
            COMMON_SETTINGS['DOMAIN'] + "/logs/" + str(self.test_run_id)
        headers = {'Content-Type': multipartblob.content_type}
        resp = self.post(log_url, data=multipartblob, headers=headers)
        logger.debug(resp.text)

    def transmit_trace(self):
        """results transmission for scopes"""
        self.session = requests.session()
        self.session.headers.update(gateway_helpers.get_headers())
        try:
            logger.debug("transmitting trace")
            # to memcache
            self.transmit_slices()
            # to the blobstore
            self.transmit_slice_blobs()
            # ToDo: Consolidate POSTs above to just one per slice

            # complete transmission indexing blobstore data
            self.test_complete()
        except Exception:
            logger.error("Exception occurred during trace transmission")
            logger.error(traceback.format_exc())
            SENTRY_CLIENT.captureException()
        finally:
            tid = self.trace_dict['test_run_id']
            gateway_helpers.post_logfile(test_run_id=tid)

    def post_result(self):
        PAYLOAD = {
            # 'result' is for the datastore entity
            'result': {
                'id': self.results_dict['test_run_id'],
                'command_id': self.results_dict['test_run_id'],
                'config': self.results_dict['config_name'],
                'instrument_type': self.results_dict['instrument_type'],
                'tags': self.results_dict['tags'],
                'plan': self.results_dict['plan'],
                'info': self.results_dict,  # ToDo: remove unnecessary values
                'dut': self.results_dict['dut'],
            },
            'fields': [{
                'name': 'config_name',
                'value': self.results_dict['config_name'],
                'type': 'text'
            },
                {
                    'name': 'hardware_name',
                    'value': self.results_dict['hardware_name'],
                    'type': 'text'
            },
                {
                    'name': 'instrument_type',
                    'value': self.results_dict['instrument_type'],
                    'type': 'text'
            },
                {
                    'name': 'test_run_id',
                    'value': self.results_dict['test_run_id'],
                    'type': 'text'
            },
                {
                    'name': 'start_datetime',
                    'value': str(datetime.now()),
                    'type': 'text'
            }
            ],
            'index_name': 'results'
        }

        url = BASE_URL + "/search"
        self.post(url, data=json.dumps(PAYLOAD))


class GRLTransmitter(ScopeTransmitter):
    """transmits data to server for GRL tests"""

    def __init__(self, transformer, trace_data):
        ScopeTransmitter.__init__(transformer, trace_data)

    def transmit_slices(self):
        # post slices
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        slice_url = BASE_URL + '/results/' + self.test_run_id + '/slices'
        voltage_start_time = 0
        dict_of_slice_lists = collections.defaultdict(int)
        ch = 'ch1'
        voltages = self.trace_dict[ch + '_voltages']
        # create list of slices
        list_of_slices = [voltages[x:x + int(CLIENT_SETTINGS['MAX_LENGTH_FOR_BROWSER'])]  # nopep8
                          for x in range(0, len(voltages), int(CLIENT_SETTINGS['MAX_LENGTH_FOR_BROWSER']))]  # nopep8
        dict_of_slice_lists[ch] = list_of_slices
        logger.debug("length of list of slices for %s: %s" %
                     (ch, len(list_of_slices)))
        for slice_index, slice_points in enumerate(list_of_slices):
            slices_by_channel = {}
            for ch in dict_of_slice_lists:
                if slice_index + 1 > len(dict_of_slice_lists[ch]):
                    logger.debug("""Warning! Slice index greater than length of
                        list of slices for %s""" % ch)
                else:
                    slices_by_channel[ch] = dict_of_slice_lists[
                        ch][slice_index]
            voltage_start_time += self.time_step * len(slice_points)
            slice_data = {
                'test_run_id': self.trace_dict['test_run_id'],
                'slice_index': slice_index,
                'num_of_slices': len(list_of_slices),
                'voltage_start_time': voltage_start_time,
                'time_step': self.time_step,
                'test_results': slices_by_channel,
            }
            slice_data = json.dumps(slice_data, ensure_ascii=True)
            if cfg.getboolean('client', 'USE_GZIP'):
                headers['content-encoding'] = 'gzip'
                slice_data = zlib.compress(json.dumps(slice_data))
            self.post(slice_url, data=slice_data, headers=headers)

    def transmit_result_blob(self, infile='grl-data.json'):
        super(GRLTransmitter, self).transmit_result_blob(infile)
