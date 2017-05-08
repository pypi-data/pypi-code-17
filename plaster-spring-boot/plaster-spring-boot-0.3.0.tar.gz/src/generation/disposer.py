import os

import src.data.types as types
from src.domain.file_information import FileInformation


def delete_file(file_info):
    abs_path = os.path.join(file_info.file_path, file_info.file_name)
    if os.path.isfile(abs_path):
        os.remove(abs_path)

        # Remove the directory if it is now empty
        if not os.listdir(file_info.file_path):
            os.rmdir(file_info.file_path)


def perform(del_type, del_name, fields):
    deletions = types.fetch_related_types(del_type)

    if not (del_name and del_type):
        return "Missing required argument"
    if not deletions:
        return "Unknown deletion type :", del_type

    files_to_delete = [FileInformation(del_name, fields, elem) for elem in deletions]
    for file_to_delete in files_to_delete:
        delete_file(file_to_delete)
