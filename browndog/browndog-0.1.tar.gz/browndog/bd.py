#!/usr/local/bin/python
import sys
import json
import urllib
import requests
import os
import time
import mimetypes
import docker
from shutil import move
from os.path import basename
from numpy import *

def get_extracted_metadata(metadata_json_ld, extractor_name):
    """
    Return a block of metadata by extractor name
    @meatadat_json_ld: it's a returned value from extract method
    @extractor_name: name of extractor. for example,"ncsa.image.ocr"
    @return a dictionary of the block with the extractor name. it contains content, @context, agent, etc.
       if it can't find one with the name, it will return None
    """
    for m in metadata_json_ld['metadata.jsonld']:
        # full uri of the name
        fullname = m['agent']['name']
        if fullname.endswith(extractor_name): 
            return m
    return None

def split_url(url):
    """
    Split URL into BrownDog Fence URL, username, and password
    @param url: URL of the BD API gateway with username and password
    @return (bds, username, password)
    """
    if '@' in url:
        parts = url.rsplit('@', 1)
        url = parts[1]
        parts = parts[0].split(':')
        username = parts[1].split('//')[1]
        password = parts[2]
        bds = parts[0] + '://' + url
        return (bds, username, password)
    else:
        return (url, '', '')


def get_key(url):
    """
    Get a key from the BD API gateway to access BD services
    @param url: URL of the BD API gateway with username and password
    @return BD API key
    """
    (bds, username, password) = split_url(url)
    r = requests.post(bds + '/keys', auth=(username, password), headers={'Accept': 'application/json'})

    if (r.status_code != 404):
        api_key = json.loads(r.text)
        return api_key['api-key']
    else:
        return ''


def get_token(url, key):
    """
    Get a token for a specific key from the BD API gateway to access BD services.
    @param url: URL of the BD API gateway with username and password
    @param key: BD API key
    @return token
    """
    (bds, username, password) = split_url(url)
    r = requests.post(bds + '/keys/' + key + '/tokens', auth=(username, password),
                      headers={'Accept': 'application/json'})

    if (r.status_code != 404):
        token = json.loads(r.text)
        return token['token']
    else:
        return ''


def outputs(bds, input, token):
    """
    Check Brown Dog Service for available output formats for the given input format.
    @param bds: The URL to the Brown Dog server to use.
    @param input: The format of the input file.
    @param token: Brown Dog access token
    @return: A string array of reachable output format extensions.
    """
    api_call = bds + '/dap/inputs/' + input
    r = requests.get(api_call, headers={'Accept': 'text/plain', 'Authorization': token})

    if (r.status_code != 404):
        return r.text.strip().split()
    else:
        return []


def convert(bds, input_filename, output, output_path, token, wait=60, verbose=False, download=True):
    """
    Convert file using Brown Dog Service.
    @param bds: The URL to the Brown Dog Server to use.
    @param input_filename: The input filename.
    @param output: The output format extension.
    @param output_path: The path for the created output file.  May contain a different filename here aswell.
    @param token: Brown Dog access token
    @param wait: The amount of time to wait for the DAP service to respond.  Default is 60 seconds.
    @param verbose: Set to true if verbose output should be generated.  Default is False.
    @param download: Set to true if download the converted file to local
    @return: The output filename if download is set to True. URL of the converted file if download is set to False
    """
    output_filename = ''
    result = ''
    boundary = 'browndog-fence-header'

    # Check for authentication
    (bds, username, password) = split_url(bds)

    try:
        if (input_filename.startswith('http://') or input_filename.startswith('https://')):
            api_call = bds + '/dap/convert/' + output + '/' + urllib.quote_plus(input_filename)
            r = requests.get(api_call, headers={'Accept': 'text/plain', 'Authorization': token})

            if (r.status_code != 404):
                result = r.text
        else:
            api_call = bds + '/dap/convert/' + output + '/'
            files = [('file', (input_filename, mimetypes.guess_type(input_filename)[0] or 'application/octet-stream'))]
            r = requests.post(api_call, headers={'Accept': 'text/plain', 'Authorization': token,
                                                 'Content-Type': 'multipart/form-data; boundary=' + boundary},
                              data=multipart([], files, boundary, 5 * 1024 * 1024))

            if (r.status_code != 404):
                result = r.text

                # print result

        if result:
            if basename(output_path):
                output_filename = output_path
            else:
                output_filename = output_path + basename(result)

            if verbose:
                print output_filename

            if download:
                download_file(result, output_filename, token, wait)
    except:
        e = sys.exc_info()[0]
        print repr(e)

    if download:
        return output_filename
    else:
        return result


def convert_local(bds, input_filename, output, output_path, token, docker_machine, wait=60, verbose=False):
    """
    Convert file using Brown Dog Service.
    @param bds: The URL to the Brown Dog Server to use.
    @param input_filename: The input filename.
    @param output: The output format extension.
    @param output_path: The path for the created output file.  May contain a different filename here aswell.
    @param token: Brown Dog access token
    @param wait: The amount of time to wait for the DAP service to respond.  Default is 60 seconds.
    @param verbose: Set to true if verbose output should be generated.  Default is False.
    @param download: Set to true if download the converted file to local
    @return: The output filename if download is set to True. URL of the converted file if download is set to False
    """
    result = ''
    docker_base_name = 'ncsapolyglot/'
    conversion_path = []
    intermediate_files = []

    # Check for authentication
    (bds, username, password) = split_url(bds)

    # Get input format
    input_format = os.path.splitext(input_filename)[1].split('.')[1]

    try:

        api_call = bds + '/dap/path/' + output + '/' + input_format
        r = requests.get(api_call, headers={'Accept': 'text/plain', 'Authorization': token})

        if r.status_code == 200:
            conversion_path = json.loads(r.text)

        # Get docker client
        docker_client = docker.Client(version='auto', **docker_machine.config(machine='default'))

        mount_dir = "/home/polyglot/data"

        # Setting intermediate input file name for chained conversions
        intermediate_output_filename = ""
        chain_count = 0

        # Get local directory and filename
        (local_dir, local_filename) = os.path.split(os.path.abspath(input_filename))

        for converter_info in conversion_path:

            # Read details about converter
            application = str(converter_info["application"])
            intermediate_output = str(converter_info["output"])
            docker_image_name = docker_base_name + "converters-" + application.lower()

            # Pull docker image if not existing locally
            status_messages = docker_client.pull(docker_image_name, tag="latest")
            if verbose:
                print status_messages

            # From second iteration onwards use output filename of the previous step as input filename of the next step
            if chain_count > 0:
                local_filename = intermediate_output_filename

            # Intermediate output filename
            intermediate_output_filename = os.path.splitext(local_filename)[0] + "." + intermediate_output

            # Create container
            docker_container = docker_client.create_container(
                user="root",
                image=docker_image_name,
                stdin_open=True,
                tty=True,
                environment={
                    "LOCAL_PROCESSING": "True",
                    "INPUT_FILE_PATH": os.path.join(mount_dir, local_filename),
                    "OUTPUT_FORMAT": intermediate_output,
                    "OPERATION": "convert",
                    "APPLICATION": application
                },
                volumes=[mount_dir],
                host_config=docker_client.create_host_config(binds=[local_dir + ":" + mount_dir])
            )

            # Store docker container ID
            docker_container_id = docker_container.get("Id")

            # Start docker container
            response = docker_client.start(container=docker_container_id)

            # Get Logs
            logs = docker_client.logs(container=docker_container_id, stdout=True, timestamps=True, stream=True)
            if verbose:
                for character in logs:
                    sys.stdout.write(character)

            # Wait for container to stop
            docker_client.wait(container=docker_container_id)

            # Remove docker container
            docker_client.remove_container(container=docker_container_id)

            # Save intermediate file names for later use
            if os.path.isfile(os.path.join(local_dir, intermediate_output_filename)):
                intermediate_files.append(intermediate_output_filename)

            chain_count += 1

        # move all intermediate files and output files to current working directory
        for file_name in intermediate_files:
            move(os.path.join(local_dir, file_name), os.path.join(os.getcwd(), file_name))

        if os.path.isfile(intermediate_output_filename):
            if basename(output_path):
                output_filename = output_path
            else:
                output_filename = output_path + basename(result)

            if verbose:
                print output_filename

            return intermediate_output_filename
    except:
        e = sys.exc_info()[0]
        print repr(e)

    return os.path.join(local_dir, intermediate_output_filename)

def download_file(url, filename, token, wait=60):
    """
    Download file at given URL.
    @param url: The URL of the file to download.
    @param filename: An optional new filename for the downloaded file.  Set to '' if the current filename on the URL is to be used.
    @param token: Brown Dog access token
    @param wait: The amount of time in seconds to wait for the file to download.  Default is 60 seconds.
    @return: The filename of the downloaded file.
    """
    if not filename:
        filename = url.split('/')[-1]

    try:
        r = requests.get(url, headers={'Authorization': token}, stream=True)

        while (wait > 0 and r.status_code == 404):
            time.sleep(1)
            wait -= 1
            r = requests.get(url, headers={'Authorization': token}, stream=True)

        if (r.status_code != 404):
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # Filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
    except:
        raise

    return filename


def extractors(bds, input, token):
    """
    Check Brown Dog Service for available extractions for the given input format.
    @param bds: The URL to the Brown Dog server to use.
    @param input: The format of the input file (not currently used!).
    @param token: Brown Dog access token
    @return: A string array of avaialble extractions.
    """
    (bds, username, password) = split_url(bds)

    # Get list of extractors
    r = requests.get(bds + '/dts/api/extractions/extractors_names',
                     headers={'Accept': 'application/json', 'Authorization': token})

    if (r.status_code != 404):
        return ', '.join(r.json()['Extractors'])
    else:
        return ''


def extract(bds, file, token, wait=60):
    """
    Extract derived data from the given input file's contents via Brown Dog Service (BDS).
    @param bds: The URL to the Brown Dog Service to use.
    @param file: The input file.
    @param token: Brown Dog Service access token
    @param wait: The amount of time to wait for the DTS to respond.  Default is 60 seconds.
    @return: The filename of the JSON file containing the extracted data.
    """
    metadata = ''
    boundary = 'browndog-fence-header'

    # Check for authentication
    (bds, username, password) = split_url(bds)

    # Upload file
    file_id = ''

    if (file.startswith('http://') or file.startswith('https://')):
        data = {}
        data["fileurl"] = file
        file_id = requests.post(bds + '/dts/api/extractions/upload_url',
                                headers={'Content-Type': 'application/json', 'Accept': 'application/json',
                                         'Authorization': token}, data=json.dumps(data)).json()['id']
    else:
        # print requests.post(bds + '/dts/api/extractions/upload_file', headers={'Accept': 'application/json', 'Authorization': token}, files={'File' : (os.path.basename(file), open(file))})
        files = [('File', (file, mimetypes.guess_type(file)[0] or 'application/octet-stream'))]
        file_id = requests.post(bds + '/dts/api/extractions/upload_file',
                                headers={'Accept': 'application/json', 'Authorization': token,
                                         'Content-Type': 'multipart/form-data; boundary=' + boundary},
                                data=multipart([], files, boundary, 5 * 1024 * 1024)).json()['id']

    # Poll until output is ready
    if file_id:
        while wait > 0:
            status = requests.get(bds + '/dts/api/extractions/' + file_id + '/status',
                                  headers={'Accept': 'application/json', 'Authorization': token}).json()
            if status['Status'] == 'Done': break
            time.sleep(1)
            wait -= 1

        # Display extracted content (TODO: needs to be one endpoint!!!)
        metadata = requests.get(bds + '/dts/api/files/' + file_id + '/tags',
                                headers={'Accept': 'application/json', 'Authorization': token}).json()
        metadata['technicalmetadata'] = requests.get(bds + '/dts/api/files/' + file_id + '/technicalmetadatajson',
                                                     headers={'Accept': 'application/json',
                                                              'Authorization': token}).json()
        metadata['metadata.jsonld'] = requests.get(bds + '/dts/api/files/' + file_id + '/metadata.jsonld',
                                                   headers={'Accept': 'application/json',
                                                            'Authorization': token}).json()
        metadata['versusmetadata'] = requests.get(bds + '/dts/api/files/' + file_id + '/versus_metadata',
                                                  headers={'Accept': 'application/json', 'Authorization': token}).json()

    return metadata


def extract_local(bds, input_filename, token, docker_machine, wait=60, verbose=False):
    """
    Extract derived data from the given input file's contents via Brown Dog Service (BDS).
    @param bds: The URL to the Brown Dog Service to use.
    @param input_file: The input file.
    @param token: Brown Dog Service access token
    @param wait: The amount of time to wait for the DTS to respond.  Default is 60 seconds.
    @return: The extracted metadata.
    """
    metadata = []
    docker_images = []

    # Check for authentication
    (bds, username, password) = split_url(bds)

    # Get MIME type of file
    mime_type, encoding = mimetypes.guess_type(input_filename)

    # MIME type could not be obtained
    if mime_type is None:
        print "Mime type of local file could not be decoded"
    # MIME type has been obtained
    else:
        # Get details about extractors running at that moment
        running_extractors = requests.get(bds + '/extractors?file_type=' + mime_type,
                                          headers={'Accept': 'application/json', 'Authorization': token}).json()

        # Iterate through the available extractors
        for extractor in running_extractors:

            # Get the docker image name for the extractor in consideration
            docker_image_name = extractor['docker_repo']

            # Continue only if docker image name is set
            if docker_image_name is not None and docker_image_name is not "":

                docker_images.append(docker_image_name)

                # Get docker client
                docker_client = docker.Client(version='auto', **docker_machine.config(machine='default'))

                # Pull docker image
                status_messages = docker_client.pull(docker_image_name, tag="latest")
                if verbose:
                    print status_messages

                # Get local directory and filename
                (local_dir, local_filename) = os.path.split(os.path.abspath(input_filename))
                ext = os.path.splitext(local_filename)[1]

                # Output filename
                output_filename = os.path.splitext(local_filename)[0] + "." + extractor['extractor_name'] + ".json"

                # Create container
                mount_dir = "/home/clowder/data"
                docker_container = docker_client.create_container(
                    user="root",
                    image=docker_image_name,
                    stdin_open=True,
                    tty=True,
                    environment={
                        "LOCAL_PROCESSING": "True",
                        "INPUT_FILE_PATH": os.path.join(mount_dir, local_filename),
                        "OUTPUT_FILE_PATH": os.path.join(mount_dir, output_filename)},
                    volumes=[mount_dir],
                    host_config=docker_client.create_host_config(binds=[local_dir + ":" + mount_dir])
                )
                docker_container_id = docker_container.get("Id")

                # Start docker container
                response = docker_client.start(container=docker_container_id)

                # Get Logs
                logs = docker_client.logs(container=docker_container_id, stdout=True, timestamps=True, stream=True)
                if verbose:
                    for character in logs:
                        sys.stdout.write(character)

                # Kill container
                docker_client.stop(container=docker_container_id)

                # Remove docker container
                docker_client.remove_container(container=docker_container_id)

                # Read JSON metadata content for the extractor, add it to metadata array, and remove extractor metadata
                # file
                output_filepath = os.path.join(local_dir, output_filename)
                if os.path.isfile(output_filepath):
                    with open(output_filepath, 'r') as json_file:
                        metadata.append(json.load(json_file))
                    os.remove(output_filepath)

    return metadata


def index(bds, directory, token, wait=60, verbose=False):
    """
    Extract signatures/tags from files via the Brown Dog Service in order to index their contents.
    @param bds: The URL to the Data Tilling Service to use.
    @param directory: The directory of files to index.
    @param token: Brown Dog Service access token
    @param wait: The amount of time per file to wait for the DTS to respond. Default is 60 seconds.
    @param verbose: Set to true if verbose output should be generated.  Default is False.
    @return: The indexed directory.  A '.index.tsv' file will now be present containing the dervied data.
    """
    if not directory.endswith('/'):
        directory += '/'

    output_filename = directory + '.index.tsv'

    with open(output_filename, 'w') as f:
        for file in os.listdir(directory):
            if not file[0] == '.':
                if verbose:
                    print file

                metadata = extract(bds, directory + file, token, wait)

                # Write to index file
                line = file

                for i in range(len(metadata['versusmetadata'])):
                    line += '\t' + str(metadata['versusmetadata'][i]['descriptor'])

                for i in range(len(metadata['tags'])):
                    line += '\t["' + str(metadata['tags'][i]) + '"]'

                f.write(line + '\n')

    return output_filename


def find(bds, query_filename, token, wait=60):
    """
    Search a directory for similar files to the query. Directory must be indexed already and a '.index.tsv' present.
    @param bds: The URL to the Brown Dog Service to use.
    @param query_filename: The query file.
    @param token: Brown Dog Service access token
    @param wait: The amount of time per file to wait for the DTS to respond. Default is 60 seconds.
    @return: The name of the file that is most similar.
    """
    ranking = {}

    # Extract signature from queury file
    metadata = extract(bds, query_filename, token, wait)

    query_descriptors = []

    for i in range(len(metadata['versusmetadata'])):
        query_descriptors.append(metadata['versusmetadata'][i]['descriptor'])

    for i in range(len(metadata['tags'])):
        tmp = []
        tmp.append(metadata['tags'][i])
        query_descriptors.append(tmp)

        # Search index
    with open('.index.tsv') as index:
        for line in index.readlines():
            parts = line.split('\t')
            file = parts[0].strip()
            descriptors = []

            for descriptor in parts[1:]:
                descriptors.append(json.loads(descriptor.strip()))

            d = descriptor_set_distance(query_descriptors, descriptors)

            ranking[file] = d

    return ranking


def descriptor_set_distance(descriptor_set1, descriptor_set2):
    """
    Calculate the closest distance between the two sets of descriptors.
    @param descriptor_set1: A set of descriptors for a file
    @param descriptor_set2: A set of descriptors for another file
    @return: The distance between the closest two descripters in each set.
    """
    d = float('inf')

    for i in range(len(descriptor_set1)):
        for j in range(len(descriptor_set2)):
            dij = descriptor_distance(descriptor_set1[i], descriptor_set2[j])

            if dij < d:
                d = dij

    return d


def descriptor_distance(descriptor1, descriptor2):
    """
    Return the distance between the two descriptors.
    @param descriptor1: A content descriptor for a file.
    @param descriptor2: A content descriptor for another file.
    @return: The distance between the two descriptors.
    """
    # Check if exactly the same
    if json.dumps(descriptor1) == json.dumps(descriptor2):
        return 0

        # Compare lists of stuff
    if isinstance(descriptor1, list) and isinstance(descriptor2, list):
        descriptor1 = array(descriptor1)
        descriptor2 = array(descriptor2)
        dimensions = len(descriptor1.shape)

        # Get distance between arrays of numbers
        if dimensions == 1 and not isinstance(descriptor1[0], basestring) and not isinstance(descriptor2[0],
                                                                                             basestring):
            return linalg.norm(descriptor1 - descriptor2)
        elif dimensions == 2 and descriptor1.shape[0] == descriptor2.shape[0]:
            n = descriptor1.shape[0]
            d = 0

            for i in range(n):
                d += linalg.norm(descriptor1[i] - descriptor2[i])

            d /= n

            return d
        else:
            return float('inf')
    else:
        return float('inf')


def multipart(data, files, boundary, blocksize=1024 * 1024):
    """Creates appropriate body to send with requests.

    The body that is generated will be transferred as chunked data. This assumes the
    following is added to headers: 'Content-Type': 'multipart/form-data; boundary=' + boundary

    Only the actual filedata is chunked, the values in the data is send as is.

    :param data: (key, val) pairs that are send as form data
    :param files:  (key, file) or (key, (file, content-type)) pairs that will be send
    :param boundary: the boundary marker
    :param blocksize: the size of the chunks to send (1MB by default)
    :return:
    """

    # send actual form data
    for tup in data:
        tup_key, tup_value = tup
        yield '--%s\r\n' \
              'Content-Disposition: form-data; name="%s"\r\n\r\n' % (boundary, tup_key)
        yield tup_value
        yield '\r\n'

    # send the files
    for tup in files:
        (tup_key, tup_value) = tup
        if isinstance(tup_value, tuple):
            real_file, content_type = tup_value
            filename = os.path.basename(real_file)
        else:
            real_file = tup_value
            filename = os.path.basename(real_file)
            content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        with open(real_file, 'rb') as fd:
            yield '--%s\r\n' \
                  'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' \
                  'Content-Type: %s\r\n\r\n' % (boundary, tup_key, filename, content_type)
            while True:
                data = fd.read(blocksize)
                if not data:
                    break
                yield data
        yield '\r\n'
    yield '--%s--\r\n' % boundary
