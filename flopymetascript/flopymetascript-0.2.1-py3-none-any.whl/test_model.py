# coding=utf-8
import glob
import io
import hashlib
import os
import zipfile
from tempfile import TemporaryDirectory

from .flopymetascript.model import Model

"""
0. process zip in to zip out
    if no serious errors occured, happy
1. unzip the input files to temporary directory
2. unzip output files to temperary directory
3. evaluate python script, model_ws -> temporary directory and write the the input files


"""

fn_in = '/Users/bfdestombe/PycharmProjects/BW/BW.zip'


def test_files_are_the_same_as_when_loaded_and_directly_written(fn_in):
    """
    If this test runs, there is no need for further che
    Should be okay to fail

    1. If the eval of the created python script results in the same
    """
    same, diff = input_files_are_the_same_as_when_loaded_and_directly_written(fn_in)
    assert len(diff) == 0, "The input files from the zip are not the same as when they are loaded and written to file"


def input_files_are_the_same_as_when_loaded_and_directly_written(fn_in):
    with open(fn_in, 'rb') as bytes_in:
        myzipfile = zipfile.ZipFile(bytes_in)

        with TemporaryDirectory() as temp_dir:
            """Automatically deletes temp_dir if an error occurs"""
            print('\nCreate temporary folder: ', temp_dir)

            for file in myzipfile.namelist():
                file_dir = myzipfile.namelist()[0]
                if file == file_dir:
                    continue

                elif file.startswith(file_dir):
                    to_path = temp_dir
                    s = 'Copying {0:s} to {1:s}'.format(file, to_path)
                    print(s)
                    myzipfile.extract(file, to_path)

            all_nam_files = glob.glob(os.path.join(temp_dir, file_dir, '*.nam')) + \
                            glob.glob(os.path.join(temp_dir, file_dir, '*.NAM'))

            assert len(
                all_nam_files) == 1, "The zip can only contain a single name file"

            _, _, filenames_input = next(os.walk(os.path.join(temp_dir, file_dir)), (None, None, []))
            print(filenames_input)

            mp = Model(all_nam_files[-1])

            with TemporaryDirectory() as temp_dir2:
                print('\nCreate temporary folder to write loaded input files: ', temp_dir2)
                mp.sw.change_model_ws(temp_dir2)
                mp.sw.write_input()

                _, _, filenames_output = next(os.walk(temp_dir2), (None, None, []))
                print(filenames_output)

                files_not_the_same = []
                files_are_the_same = []

                for fn in filenames_output:
                    path_out = os.path.join(temp_dir2, fn)
                    path_in = os.path.join(temp_dir, file_dir, fn)

                    hash_in = hashlib.md5(open(path_in, 'rb').read()).hexdigest()
                    hash_out = hashlib.md5(open(path_out, 'rb').read()).hexdigest()

                    if hash_in != hash_out:
                        files_not_the_same.append(fn)

                    else:
                        files_are_the_same.append(fn)

        print('files_are_the_same: ', files_are_the_same)
        print('files_not_the_same: ', files_not_the_same)

    return files_are_the_same, files_not_the_same


# test_files_are_the_same_as_when_loaded_and_directly_written(fn_in)

# def input_files_are_the_same_as_when_loaded_and_directly_written(fn_in):
with open(fn_in, 'rb') as bytes_in:
    myzipfile = zipfile.ZipFile(bytes_in)

    with TemporaryDirectory() as temp_dir:
        for file in myzipfile.namelist():
            file_dir = myzipfile.namelist()[0]
            if file == file_dir:
                continue

            elif file.startswith(file_dir):
                myzipfile.extract(file, temp_dir)

        all_nam_files = glob.glob(os.path.join(temp_dir, file_dir, '*.nam')) + \
                        glob.glob(os.path.join(temp_dir, file_dir, '*.NAM'))

        assert len(
            all_nam_files) == 1, "The zip can only contain a single name file"

        filenames_input = next(os.walk(os.path.join(temp_dir, file_dir)), (None, None, []))[2]
        print(filenames_input)

        mp = Model(all_nam_files[-1])

    with TemporaryDirectory() as temp_dir_sane_input, TemporaryDirectory() as temp_dir_made_input:
        print('\nCreate temporary folder to write loaded input files: ', temp_dir_sane_input)
        mp.sw.change_model_ws(temp_dir_sane_input)
        mp.sw.write_input()

        _, _, filenames_output = next(os.walk(temp_dir_sane_input), (None, None, []))
        print(filenames_output)

        print('model_ws pre ', mp.parameters['flopy.mt3d']['model_ws'])
        d = {'model_ws': temp_dir_made_input}
        mp.change_all_pack_parameter(d)
        print('model_ws post ', mp.parameters['flopy.mt3d']['model_ws'])

        s = mp.script_model2string(print_descr=False, width=99, bonus_space=0, use_yapf=False)
        print('model_ws post2 ', mp.parameters['flopy.mt3d']['model_ws'])


        # print(s)
