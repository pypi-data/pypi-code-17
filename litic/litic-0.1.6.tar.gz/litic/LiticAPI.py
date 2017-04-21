"""

.. moduleauthor:: LITIC TEAM <support@litic.com>

"""

from __future__ import print_function
from __future__ import unicode_literals

import hashlib
import zipfile
import os
import tempfile
import time
import numbers
import pandas as pd
import requests
import logging, warnings
import shutil
import datetime

from .Utils import *
from .exceptions import *

import six
from six import BytesIO
from six import StringIO

DEBUG_LEVEL = 0

# setup logging
#
# We provide a logger with the name of this module. Then calling
# application can get the logger and attach a handler to it.
# See https://docs.python.org/2/howto/logging.html
logger = logging.getLogger(__name__)


class _LiticSession:

    def __init__(self):
        self.session = requests.Session()

    def post_form(self, url, params):
        logger.info("Posting to url %s", url)
        logger.debug("Parameters: %s", str(params))
        try:
            r = self.session.post(url, data=params)
            r.raise_for_status()
        except Exception as e:
            # try to get the description from the json. Use the string
            # of the current exception if this does not work
            msg = str(e)
            try:
                r.json()
                msg = "HTTP return code %d: %s\n\n%s" % (r["status"],
                                                         r["title"],
                                                         r["description"])
            except:
                pass
            raise LiticConnectionError(msg)
        r.encoding = "utf-8"
        logger.debug("Response: %s", r.text)
        return r.text

    def post_json(self, url, data=None):
        logger.info("Posting json data to url %s", url)
        logger.debug("Data: %s", data)
        try:
            r = self.session.post(url, json=data)
            r.raise_for_status()
        except Exception as e:
            # try to get the description from the json. Use the string
            # of the current exception if this does not work
            msg = str(e)
            try:
                r.json()
                msg = "HTTP return code %d: %s\n\n%s" % (r["status"],
                                                         r["title"],
                                                         r["description"])
            except:
                pass
            raise LiticConnectionError(msg)
        r.encoding = "utf-8"
        logger.debug("Response: %s", r.text)
        return r.json()

    def post_zip(self, url, filehandle):
        files = {'file': ('box.zip',
                          filehandle,
                          'application/zip',
                          {'Expires': '0'})}
        logger.info("Posting zip file to url %s", url)
        try:
            r = self.session.post(url, files=files)
            r.raise_for_status()
        except Exception as e:
            # try to get the description from the json. Use the string
            # of the current exception if this does not work
            msg = str(e)
            try:
                r.json()
                msg = "HTTP return code %d: %s\n\n%s" % (r["status"],
                                                         r["title"],
                                                         r["description"])
            except:
                pass
            raise LiticConnectionError(msg)
        r.encoding = "utf-8"
        logger.debug("Response: %s", r.text)
        return r.text

    def get_url_text(self, url):
        logger.info("Getting url %s as text", url)
        try:
            r = self.session.get(url)
            r.raise_for_status()
        except Exception as e:
            # try to get the description from the json. Use the string
            # of the current exception if this does not work
            msg = str(e)
            try:
                r.json()
                msg = "HTTP return code %d: %s\n\n%s" % (r["status"],
                                                         r["title"],
                                                         r["description"])
            except:
                pass
            raise LiticConnectionError(msg)
        r.encoding = "utf-8"
        logger.debug("Response: %s", r.text)
        return r.text

    def post_url_json(self, url, data=None):
        logger.info("Getting url %s as json", url)
        try:
            r = self.session.post(url, json=data)
            r.raise_for_status()
        except Exception as e:
            # try to get the description from the json. Use the string
            # of the current exception if this does not work
            msg = str(e)
            try:
                r.json()
                msg = "HTTP return code %d: %s\n\n%s" % (r["status"],
                                                         r["title"],
                                                         r["description"])
            except:
                pass
            raise LiticConnectionError(msg)

        r.encoding = "utf-8"
        logger.debug("Response: %s", r.text)
        return r.json()

    def get_url_raw(self, url):
        logger.info("Getting url %s as raw", url)
        try:
            r = self.session.get(url, stream=True)
            r.raise_for_status()
        except Exception as e:
            # try to get the description from the json. Use the string
            # of the current exception if this does not work
            msg = str(e)
            try:
                r.json()
                msg = "HTTP return code %d: %s\n\n%s" % (r["status"],
                                                         r["title"],
                                                         r["description"])
            except:
                pass
            raise LiticConnectionError(msg)
        return r.raw


    def stream_url(self, url, filename):
        logger.info("Streaming response of url %s to %s", url, filename)
        handle = self.get_url_raw(url)

        # r.raw is a file object, so we can directly copy it
        # Taken from http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
        with open(filename, 'wb') as f:
            shutil.copyfileobj(handle, f)

class _LiticConnection:

    def __init__(self, serviceurl, apikey):
        """
        Parameters
        ----------
        serviceurl: The URL contains the service part in the form of [http|https]://host:port/path/
        apikey: API Key
        """
        if (serviceurl[-1] == '/'):
            serviceurl = serviceurl[:-1]
        self.serviceurl = serviceurl
        self.apikey = apikey
        self.files = []
        self.loggedin = False
        self.session = _LiticSession()

    def get_service_info(self):
        urlpath = self.serviceurl + "/info"
        response = self.session.post_url_json(urlpath)
        return response

    def login(self):

        # don't do anything if we are logged in already
        if self.loggedin:
            return

        if DEBUG_LEVEL > 1:
            print("Login", self.serviceurl + "/servicelogin/")
        response = self.session.post_json(self.serviceurl + "/login",
                                          {"api_key": self.apikey})
        if DEBUG_LEVEL > 2:
            print("response: ", response)

        statusval = response["status"]
        if (statusval == "ok"):
            self.loggedin = True
        else:
            raise LiticRuntimeError(
                "Can not login to LITIC server, please check your URL and API_KEY")


    def upload_zip(self, file_or_buf):
        """Uploads a given zip archive

        The method permits to upload a file on disc by passing the
        file name or a stream that is in memory by passing the stream object.

        :param file: Filename or open file-like object to be uploaded
        """

        response = self.session.post_zip(
            self.serviceurl + "/uploadfiles", file_or_buf)
        if DEBUG_LEVEL > 4:
            print(response)

    def start_procedure(self, data):
        response = self.session.post_json(
            self.serviceurl + "/start",
            data)
        if response["status"] != "ok":
            raise LiticConnectionError(response["description"])
        return response["job_id"]


    def send_check_files(self, data):
        response = self.session.post_json(
            self.serviceurl + "/checkfiles", data)
        if DEBUG_LEVEL > 4:
            print("check files resp: ", response)
        return response

    def post_job_status(self, jobid):
        url = self.serviceurl + "/status"
        response = self.session.post_url_json(url, {"job_id": jobid})
        if DEBUG_LEVEL > 4:
            print("status resp: ", response)
        return response

    def download_output_to_file(self, jobid, filename, outpath):
        url = "%s/download/%s/%s" % (self.serviceurl, jobid, filename)
        self.session.stream_url(url, outpath)

    def get_output_file(self, jobid, filename):
        url = self.serviceurl + "/download/" + jobid + "/" + filename
        url = str(url)  # curl doesn't like unicode
        return self.session.get_url_raw(url)

    def sha1_file(self, filename):
        sha1 = hashlib.sha1()
        with open(filename, 'rb') as content_file:
            content = content_file.read()
            sha1.update(content)
        return sha1.hexdigest()

    def sha1_stream(self, stream):
        """Get sha1 for a StringIO or a BytesIO"""
        sha1 = hashlib.sha1()
        stream.seek(0)
        if isinstance(stream, BytesIO):
            sha1.update(stream.read())
        else:
            sha1.update(stream.read().encode('utf-8'))
        stream.seek(0)
        return sha1.hexdigest()


class LiticService:
    """The class to call LITIC procedures.

    :param serviceurl: The base URL to the service.
    :param apikey: The API key for authentication
    :param input_to_disc: Try to write temporary files to disc instead of holding them in memory

    """

    def __init__(self, serviceurl, apikey, input_to_disc=False):
        self.input_to_disc = input_to_disc

        self.connection = _LiticConnection(serviceurl, apikey)

        self.cube_map = {}
        self.scalar_map = {}
        self.last_jobid = None
        self.last_procedure = None

        # log in to server
        self.connection.login()

        # get info about the services
        self.info = self.connection.get_service_info()
        self.procedures = {proc["name"]: proc for proc in self.info["procedures"]}

        # maintain a list of temporary files that need be deleted
        self.files_to_delete = []

    # read CSV that has headers to XML format
    def _CSV_with_headers_to_XML(self, inputfile, inputinfos, loaded_cubes):
        # find out the available cubes in the CSV file

        if isinstance(inputfile, (BytesIO, StringIO)):
            inputfile.seek(0)
            f = inputfile
        else:
            if six.PY3:
                f = open(inputfile, "r")
            else:
                f = open(inputfile, "rb")

        # deduce from first line
        try:
            reader = unicode_csv_reader(f, skipinitialspace=True)
            header = six.next(reader)
        except:
            raise LiticInputError("File " + inputfile + " is not a valid CSV file")
        cubelist = []
        columns = []
        if header[0] == "(Scalar Name)":
            for i, row in enumerate(reader):
                n_row, n_type = extract_header_format(row[0])
                cubelist.append(n_row)
                columns.append(n_row)
        else:
            header = [h.strip() for h in header]
            for column in header:
                col = column.strip()
                n_col, n_type = extract_header_format(col)
                if n_col in [inp["name"] for inp in inputinfos]:
                    cubelist.append(n_col)
                elif n_col.find('(') == 0 and n_col.find(')') == len(n_col) - 1:
                    n_col = n_col[1:len(n_col) - 1]
                columns.append(n_col)
        for fname in loaded_cubes:
            otherlist = loaded_cubes[fname]
            for current_col in cubelist:
                if current_col in otherlist:
                    raise LiticInputError("Cube '%s' is defined in more than one input."
                                          % current_col)
        loaded_cubes[inputfile] = cubelist
        unrecognized_names = []
        all_names = set()
        if DEBUG_LEVEL > 4:
            print("READ: %s" % ",".join(cubelist))
        for inp in inputinfos:
            all_names.add(inp["name"])
            if "dimensions" in inp:
                for d in inp["dimensions"]:
                    all_names.add(d)
        for column in columns:
            if column not in all_names:
                unrecognized_names.append(column)
        # if (len(cubelist)==0):
        # print("Warning: Cubes required for inputs are not sent:",
        # inputinfos)
        # if len(unrecognized_names) > 0:
        #     warnings.warn("Warning: Unrecognized data names: %s" % unrecognized_names)

        # check all dimensions of the cube are in the csv file
        for cube in cubelist:
            inp = [inp for inp in inputinfos if inp["name"] == cube][0]
            if "dimensions" not in inp:
                continue
            for dimension in inp["dimensions"]:
                if dimension not in columns:
                    raise LiticInputError(
                        "Cube '%s' requires dimension '%s' but is not in the CSV file"
                        % (cube, dimension))

        # reset stream or close file
        if isinstance(inputfile, (BytesIO, StringIO)):
            inputfile.seek(0)
        else:
            f.close()

    def _generate_csv(self, input, filehashes, filenames, scalars, in_memory=True):
        """Converts the given input to csv

        Returns either a filename to which the csv has been written or
        a BytesIO buffer with the csv content. If a temporary file was
        written, its name is added to the self.files_to_delete list.
        """

        if isinstance(input, tuple):
            # if we have a tuple (string, Scalar), then create a DataFrame and
            # reassign it to input
            if (len(input) == 2 and
                (isinstance(input[1], numbers.Number) or
                 isinstance(input[1], str))):
                scalars[input[0]] = input[1]
                return
            else:
                raise LiticInputError("Inputs contain invalid data type")

        if not isinstance(input, pd.DataFrame):
            raise LiticInputError("Inputs contain invalid data type <%s>" % type(input))

        # from now on we have a DataFrame
        if in_memory:
            if six.PY3:
                stream = StringIO()
            else:
                stream = BytesIO()
            input.to_csv(stream, encoding='utf-8')
            filehashes[stream] = self.connection.sha1_stream(stream)
            filenames[stream] = "%s.csv" % filehashes[stream]
        else:
            f, tpath = tempfile.mkstemp(suffix=".csv")
            os.close(f)
            input.to_csv(tpath, encoding='utf-8')
            self.files_to_delete.append(tpath)
            filehashes[tpath] = self.connection.sha1_file(tpath)
            filenames[tpath] = os.path.basename(tpath)

    def _upload_missing_files(self, missing, filenames, in_memory=False):

        # early exit if no files are actually missing
        if not missing:
            return

        if in_memory:
            handle = BytesIO()
        else:
            fd, zipfilename = tempfile.mkstemp(suffix='.zip')
            # wrap the file description return by mkstemp in a file-like object
            handle = os.fdopen(fd, 'wb')

        if len(set(filenames.values())) != len(filenames):
            raise LiticRuntimeError("The names of the files to be uploaded are not unique. "
                                    "This should not happen!")

        logger.debug("Missing files are: %s", str(missing))
        logger.debug("Available files are: %s", str(filenames))

        # pack the zip file with the missing files. Iterate over all
        # known files and filter those that are missing
        with zipfile.ZipFile(handle, 'w') as myzip:
            for file_or_buf, name in six.iteritems(filenames):
                if name not in missing:
                    if file_or_buf in self.files_to_delete:
                        logger.debug("Deleting temporary file %s", file_or_buf)
                        os.remove(file_or_buf)
                        self.files_to_delete.remove(file_or_buf)
                    continue
                if isinstance(file_or_buf, BytesIO):
                    file_or_buf.seek(0)
                    logger.debug("Adding BytesIO under name %s", name)
                    myzip.writestr(name, file_or_buf.read(),
                                   zipfile.ZIP_DEFLATED)
                elif isinstance(file_or_buf, StringIO):
                    file_or_buf.seek(0)
                    logger.debug("Adding StringIO under name %s", name)
                    myzip.writestr(name,
                                   file_or_buf.read().encode('utf-8'),
                                   zipfile.ZIP_DEFLATED)
                else:
                    logger.debug("Adding file <%s> under name %s",
                                 file_or_buf, name)
                    myzip.write(file_or_buf,
                                name, zipfile.ZIP_DEFLATED)
                    if name in self.files_to_delete:
                        logger.debug("Deleting temporary file %s", name)
                        os.remove(name)
                        self.files_to_delete.remove(name)

        # reset or reopen the zip file
        if in_memory:
            handle.seek(0)
        else:
            handle = open(zipfilename, 'rb')

        # perform the upload
        response = self.connection.upload_zip(handle)
        if DEBUG_LEVEL > 4:
            print(response)

        handle.close()

        # delete the temporary file
        if not in_memory:
            os.remove(zipfilename)

    def _get_last_jobid(self):
        """
        :return: The latest job id.
        :rtype: str
        """
        return self.last_jobid

    def  _check_input_files(self, input_files):

        if input_files is None:
            return []

        if not isinstance(input_files, list):
            input_files = [input_files]

        if not all(isinstance(x, str) for x in input_files):
            raise LiticInputError(
                "input_files can be only a string or a list of strings")
        if (len(set(map(os.path.basename, input_files))) != len(input_files)):
            raise LiticInputError(
                "There are duplicates in the input cube file list")
        missing = []
        for f in input_files:
            if not os.path.exists(f):
                missing.append(f)
        if (len(missing) > 0):
            raise LiticInputError(
                "The following files are missing: %s" % ", ".join(missing))

        return input_files

    def get_procedures(self):
        """ Return the procedures that are available in this service

        :return: The procedure list
        :rtype: list
        """
        return list(self.procedures.keys())

    def run_procedure(self,
                      procedure_name=None,
                      input=None,
                      input_files=None,
                      timeout=300):
        """The central message to run a procedure.

        Inputs can be provided in several ways. Either by one of these options in the ``input`` argument:

        * tuple (id, value): pass a value to a scalar with a given id.
        * tuple (id, dict(dims -> value)): pass the content of the dict into a cube. dims can be an identifier or a tuple of the dimensions of the input cube.
        * pandas.DataFrame: The dimensions and the cubes are derived from the names of the columns and from the names of the index/multiindex. Only data that has the same dimensions can be passed in the same DataFrame. Columns that are not recognized as dimension or cube are ignored, but a warning is issued.

        Alternatively, you can providing names of .csv files in the
        ``input_files`` argument. This is advisable if the data is
        available in this format anyway or if the data is too large to
        fit into the memory of you local machine. The column headers
        in the files are interpreted as the cube/dimension names.
        Columns that cannot be interpreted as dimension or cube are
        ignored and a warning is issued.

        :param str procedure_name: The name of the procedure to be called.
        :param input: One or a list of the above stated arguments.
        :param input_files: One or a list of filenames of csv input files.
        :param timeout: Seconds to wait for results. After that a ``LiticProcedureTimeout`` is raised.

        """
        self.last_jobid = None
        self.last_procedure = None
        if (procedure_name is None):
            raise LiticRuntimeError("Procedure name can not be None")
        if (procedure_name.strip() == ""):
            raise LiticRuntimeError("Procedure name can not be empty string")
        if timeout < 1:
            timeout = 1

        # get the info about this proc
        if procedure_name not in self.procedures:
            raise LiticRuntimeError("Procedure name <%s> not found" % procedure_name)
        procedure = self.procedures[procedure_name]

        input_files = self._check_input_files(input_files)
        filehashes = {f: self.connection.sha1_file(f) for f in input_files}
        filenames = {f: os.path.basename(f) for f in input_files}

        # check and convert input to files or buffers
        scalars = {}
        if input is not None:
            if not isinstance(input, list):
                input = [input]
            for inp in input:
                self._generate_csv(inp, filehashes, filenames, scalars, in_memory=not self.input_to_disc)

        loaded_cubes = {}
        for file_or_buf, name in six.iteritems(filenames):
            self._CSV_with_headers_to_XML(file_or_buf, procedure["inputs"],
                                          loaded_cubes)

        cubefiles = { filenames[f] : filehashes[f] for f in filenames.keys()}
        known_missing = self.connection.send_check_files({ "cube_files" : cubefiles })
        self._upload_missing_files(known_missing["unknown_files"],
                                   filenames,
                                   in_memory=not self.input_to_disc)

        data = {"procedure": procedure_name,
                "cube_files": list(filenames.values()),
                "scalars": scalars,
                "timeout": timeout}

        self.last_jobid = self.connection.start_procedure(data)
        self.last_procedure = procedure_name

        # wait until we have a job status that signals we are done
        waited = 0
        while waited < timeout:

            # determine the time we want to wait
            if waited == 0:
                wait = 0
            elif waited < 100:
                wait = 1
            elif waited < 500:
                wait = 15
            else:
                wait = 60
            # we always want to respect the timeout.
            wait = min(wait, timeout - waited)

            time.sleep(wait)
            waited += wait

            # check the job status and break the waiting loop if we are done
            job_status = self.connection.post_job_status(self.last_jobid)
            if (job_status["status"] in ["Done", "Error", "Timeout", "Canceled"]):
                break

        # handle timeout
        if waited >= timeout or job_status["status"] == "Timeout":
            raise LiticProcedureTimeout("Procedure '%s' has timed out."
                                        % (procedure_name))

        # handle error
        if job_status["status"] == "Error":
            self.cube_map = {}
            self.scalar_map = {}
            raise LiticRuntimeError(job_status["description"])

        # handle canceled
        if job_status["status"] == "Canceled":
            self.cube_map = {}
            self.scalar_map = {}
            return

        # handle normal termination of procedure
        assert(job_status["status"] == "Done")

        # fetch available outputs and fix types of all scalars, so we can never forget to do this
        self.cube_map = job_status["cubes"]
        self.scalar_map = {name: self._fix_scalar_type(name, value)
                           for name, value in six.iteritems(job_status["scalars"])}

    def _fix_scalar_type(self, name, value):

        # if the value is missing, we don't do anything
        if value is None:
            return value

        # get info about the last procedure that was executed
        proc = self.procedures[self.last_procedure]

        # get the type this scalar has to have
        candidates = [out for out in proc["outputs"] if out["name"] == name]
        assert(len(candidates) == 1)
        value_type = candidates[0]["value_type"]

        if value == "" :
            return value

        if value_type == "Integer":
            return int(value)
        elif value_type == "Real":
            return float(value)
        elif value_type in ["Binary", "Unary"] :
            return bool(value)
        elif value_type == "Date":
            return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            return value


    def get_available_cubes(self):
        """Get the names of available output cubes.

        This method considers only the output cubes that can
        actually be retrieved from the service. It returns the empty
        list if no procedure has successfully terminated.

        :return: The names of available output cubes.
        :rtype: list
        """
        return self.cube_map.keys()


    def get_available_scalars(self):
        """Get the names of available output scalars.

        This method considers only the output scalars that can
        actually be retrieved from the service. It returns the empty
        list if no procedure has successfully terminated.

        :return: The names of available output scalars
        :rtype: list
        """
        return self.scalar_map.keys()


    def get_cube(self, cubename, filename=None):
        """ Download an output cube.

        If the ``filename`` is specified, the csv representation of the cube
        will be streamed into the given file. Otherwise, the cube is returned as
        ``pandas.DataFrame``.

        :param str cubename: The name of the cube
        :param str filename: The name of an output file (optional)
        """
        if not self.last_jobid:
            raise LiticOutputError("No job has been done. No results available.")
        try:
            download_filename = self.cube_map[cubename]
        except KeyError:
            raise LiticOutputError("Unknown output cube <%s>." % cubename)

        if filename:
            self.connection.download_output_to_file(self.last_jobid, download_filename, filename)
        else:
            handle = self.connection.get_output_file(self.last_jobid, download_filename)
            df = pd.read_csv(handle)
            return df


    def get_scalar(self, scalar_name=None):
        """Get the value of one, several, or all known scalars

        If a string is given, the value of that scalar will be returned. If an
        iterable is given, a dictionary {scalar name -> value} is returned. If
        called without arguments, a dict containing all scalar outputs is
        returned.

        :param scalar_name: One or an iterable of names of scalar outputs.
        :return: The scalar value if only one name was passed or a dict {id -> value} if several names were passed
        """
        if not self.last_jobid:
            raise LiticOutputError("Not job has been done. No results available.")

        if scalar_name is None:
            return self.scalar_map.copy()

        if isinstance(scalar_name, six.string_types):
            return self.scalar_map[scalar_name]

        return {name: self.scalar_map[name] for name in scalar_name}

    def get_scalar_file(self, filename):
        """ Download the output scalars.

        If the ``filename`` is specified, the csv representation of the scalars
        will be streamed into the given file.

        :param str filename: The name of an output file
        """
        if not self.last_jobid:
            raise LiticOutputError("No job has been done. No results available.")

        if self.get_available_scalars() < 1 :
            raise LiticOutputError("No scalar results available.")

        download_filename = "scalars.csv"
        self.connection.download_output_to_file(self.last_jobid, download_filename, filename)
