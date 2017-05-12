from ...exceptions import RuntimeError
import os, shutil, json, zipfile


def format_output(*args):
    """
    Format the output.
        @param:
            - args: the strings to format

        @result: format the given string as following '[string1:string2:....:stringN]:'
    """
    result = "["
    for arg in args:
        result += str(arg)
        result += str(":")
    return result[:-1] + str("]: ")


def remove_file(path):
    """
    Removes the given file if it exists, raise an error otherwise.
        @param:
            - path: string (/path/to/the/file/to/remove)

        @behave: raise an error if the specified file does not exist.
    """
    if os.path.isfile(path) == True:
        os.remove(path)
    else:
        raise RuntimeError(__name__, remove_file.__name__, "Cannot remove (" + path + "), no such file.")


def remove_directory(path):
    """
    Handler for removing a directory and all its content
        @param:
            - path: string (/path/to/the/directory/to/remove)

        @behave: raise an error if the specified directory does not exist.
    """
    if os.path.isdir(path) == True:
        shutil.rmtree(path)
    else:
        raise RuntimeError(__name__, remove_directory.__name__, "Cannot remove (" + path + "), no such directory.")


def unzip(path, destination):
    """
    Unzip the file pointed by 'path' to extract its to content to the given destination
        @params:
            - path: string (/path/to/the/file/to/unzip)
            - destination: string (/path/to/extract/the/zip)

        @behave: raise an error if either the path or the destination is invalid.
        @behave: raise an error if the archive is corrupted.
    """
    if os.path.isfile(path) == True:

        if os.path.isdir(destination) == True:
            archive = zipfile.ZipFile(path, 'r')
            result = archive.testzip()

            if result is not None:
                raise RuntimeError(__name__, unzip.__name__, "Error corrupted archive.")

            archive.extractall(destination)
            archive.close()

        else:
            raise RuntimeError(__name__, unzip.__name__, "Invalid path (" + destination + "), no such directory.")
    else:
        raise RuntimeError(__name__, unzip.__name__, "Invalid path (" + path + "), no such file.")


def parse_json_file_to_dictionary(path, dictionary):
    """
    Parse a json file and store key and value into the given dictionary.
        @params:
            - path: string (/path/to/the/directory/containing/the/json/file)
            - dictionary: the dictionary to fill with data.

        @behave: raise an error if the path is not pointing to a directory.
    """
    if os.path.isdir(path) == True:
        for file in os.listdir(path):
            if file.find(".json") > 0:
                with open(path + '/' + file) as json_file:
                    data = json.load(json_file)
                for key, value in data.items():
                    dictionary[key] = value
    else:
        raise RuntimeError(__name__, parse_json_file_to_dictionary.__name__, "Invalid path (" + path + "), no such directory.")
