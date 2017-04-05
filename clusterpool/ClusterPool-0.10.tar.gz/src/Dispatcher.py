"""
Created on Wed May 20 15:20:35 2015

@author: joseph
"""
import os
import time
import math
import random
import hickle
import cPickle as pickle
import datetime
import subprocess
import warnings
import shutil
import numpy as np


SLURM_TEMP_FILE_STORAGE_DIRECTORY = "/n/regal/aspuru-guzik_lab/jgoodknight/"

class Dispatcher(object):

    TEMPLATE_FILE_PYTHON_CALCULATION = os.path.dirname(os.path.realpath(__file__)) + "/GENERAL/python_calculation.template"
    TEMPLATE_FILE_PYTHON_TRAWLER = os.path.dirname(os.path.realpath(__file__)) + "/GENERAL/python_trawler.template"

    TEMPLATE_FILE_NAME = "$FILE_NAME"
    TEMPLATE_FUNCTION_NAME = "$FUNCTION_NAME"
    TEMPLATE_SPECIAL_SAVE_LOCATION = "$SPECIAL_SAVE_LOCATION"
    TEMPLATE_NORMAL_SAVE_BOOL = "$NORMAL_SAVE"


    statically_saved_filenames = set()

    def __init__(self):
        self.starting_date = str(datetime.date.today())
        self.current_id_number = 0

        try:
            os.mkdir(self.TEMP_FILE_STORAGE_DIRECTORY)
            print("temp directory created!")
        except OSError:
            print("temp directory already exists")


        while True:
            dispatcher_id = random.randint(10000, 99999)
            try:
                file_dir_str = self.TEMP_FILE_STORAGE_DIRECTORY + str(dispatcher_id)
                print(file_dir_str)
                os.mkdir(file_dir_str)
                break
            except OSError:
                continue
        self.dispatcher_id = dispatcher_id

        tempFile = open(SLURM.TEMPLATE_FILE_PYTHON_CALCULATION, 'rb')
        self.python_calculation_template_string = tempFile.read()
        tempFile.close()

        self.process_id_TO_filename = {}

        try:
            os.mkdir(self.file_directory())
        except OSError:
            print "directory already made"

    def save_python_object_file_return_id(self, object_to_save):
        ID_number = self.__generate_id_number__()
        fileToBeSaved = open(self.object_filename(ID_number), 'wb')
        pickle.dump(object_to_save, fileToBeSaved)
        fileToBeSaved.close()

        return ID_number

    @staticmethod
    def save_shared_object_return_filename(python_object, name_string):
        try:
            os.mkdir(Dispatcher.TEMP_FILE_STORAGE_DIRECTORY)
        except OSError:
            print "directory already made"
        filename = Dispatcher.TEMP_FILE_STORAGE_DIRECTORY + name_string + str(np.random.randint(100000)) + ".pkl"
        while filename in Dispatcher.statically_saved_filenames:
            filename = Dispatcher.TEMP_FILE_STORAGE_DIRECTORY + name_string + str(np.random.randint(100000)) + ".pkl"
        fileToBeSaved = open(filename, 'wb')
        pickle.dump(python_object, fileToBeSaved)
        fileToBeSaved.close()
        Dispatcher.statically_saved_filenames.add(filename)
        return filename

    def file_directory(self):
        return self.TEMP_FILE_STORAGE_DIRECTORY + str(self.dispatcher_id) + "/"

    def base_filename(self, id_number):
        return self.file_directory() + str(id_number)

    def python_filename(self, id_number):
        return self.file_directory() + str(id_number) + ".py"

    def object_filename(self, id_number):
        return self.file_directory() + str(id_number) + ".uncalculated.pkl"

    def error_filename(self, id_number):
        return self.file_directory() + str(id_number) + ".err"

    def output_filename(self, id_number):
        return self.file_directory() + str(id_number) + ".out"

    def calculated_object_filename(self, id_number):
        return self.file_directory() + str(id_number) + ".CALCULATED.pkl"

    def bash_script_filename(self, id_number):
        return self.file_directory() + "script_" + str(id_number) + ".sh"

    def __is_id_used__(self, id_number):
        return os.path.isfile(self.object_filename(id_number))

    def __generate_id_number__(self):
        while True:
            new_id = self.current_id_number + 1
            self.current_id_number = new_id
            if self.__is_id_used__(new_id):
                continue
            else:
                self.current_id_number = new_id
                return new_id

    def is_process_finished(self, ID_number):
        return os.path.isfile(self.calculated_object_filename(ID_number))

    def return_calculated_object(self, ID_number):
        if not self.is_process_finished(ID_number):
            raise Exception("process is not finished yet!")
        filename = self.calculated_object_filename(ID_number)
        myFile = open(filename, 'rb')
        output = pickle.load(myFile)
        myFile.close()
        return output

    def delete_all_temp_files(self, ID_number):
#        os.remove(self.python_filename(ID_number))
#        os.remove(self.object_filename(ID_number))
        os.remove(self.calculated_object_filename(ID_number))
#        os.remove(self.output_filename(ID_number))
#        os.remove(self.error_filename(ID_number))
#        os.remove(self.bash_script_filename(ID_number))

    def cancel_unfinished_processes(self):
        pass

    def kill_dispatcher(self):
        try:
            shutil.rmtree(self.file_directory())
            self.cancel_unfinished_processes()
        except:
            warnings.warn("error found in kill_dispatcher!")

    def start_subprocess_trawlers(self, number):
        for i in range(number):
            self.__start_subprocess_trawler__(i)

    def __start_process__(self, ID_number):
        raise Exception("abstract method must be implemented!")
    def __initiate_bash_shell_command__(self, ID_number):
        raise Exception("abstract method must be implemented!")



class SLURM(Dispatcher):
    id_string = "SLURM"
    TEMP_FILE_STORAGE_DIRECTORY = SLURM_TEMP_FILE_STORAGE_DIRECTORY
    PENDING = 'PENDING'
    TIMEOUT = 'TIMEOUT'
    CANCELLED = 'CANCELLED'
    NODE_FAIL = 'NODE_FAIL'
    PREEMPT = 'PREEMPTED'
    SUSPENDED = 'SUSPENDED'
    FAILED = 'FAILED'
    BOOT_FAIL = 'BOOT_FAIL'
    COMPLETED = 'COMPLETED'
    CONFIGURING = 'CONFIGURING'
    COMPLETING = 'COMPLETING'
    PREEMPTED = 'PREEMPTED'
    RESIZING = 'RESIZING'

    TEMPLATE_NUMBER_CORES = "$NUMBER_CORES"
    TEMPLATE_NUMBER_MINUTES = "$NUMBER_MINUTES"
    TEMPLATE_QUEUE_NAME = "$QUEUE_NAME"
    TEMPLATE_MEMORY_MB = "$MEMORY_MB"
    TEMPLATE_OUTPUT_FILE_NAME = "$OUTPUT_FILENAME"
    TEMPLATE_PYTHON_SCRIPT_NAME = "$PYTHON_SCRIPT_NAME"


    TEMPLATE_DIRECTORY_NAME = "$DIRECTORY_NAME"
    TEMPLATE_NUMBER = "$NUMBER"


    DEFAULT_QUEUE_NAME = "aspuru-guzik"

    TEMPLATE_FILE_SCRIPT_SUBMISSION = os.path.dirname(os.path.realpath(__file__)) + "/SLURM/slurm_submission_script.template"

    dispatcher_id_TO_cluster_process_id = {}

    TIMEOUT_FAILURE_TIME_MULTIPLIER = 1.05
    TARGET_PROCESS_TIMES_MINUTES = 60.0

    MAX_CLUSTER_START_ATTEMPTS = 100

    RESTART_WAITING_TIME_MINUTES = 5.0

    restart_counts = {}
    MAX_RESTART_COUNT = 25



    def __init__(self, time_requested_minutes, memory_requested_MB, number_of_cores = 1, number_of_machines = 1, partition_name = None):
        super(SLURM, self).__init__()

        if partition_name == None:
            partition_name = SLURM.DEFAULT_QUEUE_NAME
        self.partition_name = partition_name

        self.time_requested_minutes = int(math.ceil(time_requested_minutes))
        if self.time_requested_minutes == 0:
            self.time_requested_minutes = 1
        self.memory_requested_MB = int(memory_requested_MB)
        self.number_of_cores = number_of_cores
        self.number_of_machines = number_of_machines

        self.number_calculations_per_core = int(SLURM.TARGET_PROCESS_TIMES_MINUTES / self.time_requested_minutes )
        self.__process_sent_off_count__ = 0


        print "will send %s calculations to each core" % str(self.number_calculations_per_core)

        self.time_requested_minutes = self.time_requested_minutes * (self.number_calculations_per_core + 1) + 5

        self.update_bash_submission_string()

        self.dispatcher_id_TO_cluster_process_id = {}

        self.cluster_process_ids = []

        try:
            os.mkdir(Dispatcher.TEMP_FILE_STORAGE_DIRECTORY)
        except OSError:
            pass

    def __start_subprocess_trawler__(self, number):
        f = open(Dispatcher.TEMPLATE_FILE_PYTHON_TRAWLER, "rb")
        python_file_text = f.read()
        f.close()
        python_file_text = python_file_text.replace(SLURM.TEMPLATE_NUMBER, str(number))
        python_file_text = python_file_text.replace(SLURM.TEMPLATE_DIRECTORY_NAME, self.file_directory())

        trawler_id = "d" + str(self.dispatcher_id) + "_T" + str(number)

        python_file = open(self.file_directory() + trawler_id + ".py", "wb")
        python_file.write(python_file_text)
        python_file.close()

        bash_script_text = self.bash_submission_template_string.replace(SLURM.TEMPLATE_PYTHON_SCRIPT_NAME, self.file_directory() + trawler_id + ".py")
        bash_script_text = bash_script_text.replace(SLURM.TEMPLATE_OUTPUT_FILE_NAME, self.file_directory() + trawler_id)
        bash_script_file = open(self.file_directory() + trawler_id + ".sh", "wb")
        bash_script_file.write(bash_script_text)
        bash_script_file.close()

        command = ["sbatch", self.file_directory() + trawler_id + ".sh"]
        process_started = False
        attempt_count = 0
        while process_started == False:
            attempt_count = attempt_count + 1
            try:
                output  = subprocess.check_output(command)
                cluster_process_id = output.split()[3]
                try:
                    cluster_id = int(cluster_process_id)
                    self.cluster_process_ids.append(cluster_id)
                except ValueError:
                    warnings.warn("CLUSTER FAILED TO START JOB, TRYING AGAIN")
                    time.sleep(SLURM.RESTART_WAITING_TIME_MINUTES * 60)
                    continue
                process_started = True
            except subprocess.CalledProcessError, e:
                print e.output
                if attempt_count < SLURM.MAX_CLUSTER_START_ATTEMPTS:
#                    print "trying again to start process %s" % str(ID_number)
                    time.sleep(SLURM.RESTART_WAITING_TIME_MINUTES * 60)
                    continue
                else:
                    raise Exception("The number of restart attempts for trawler %s is TOO DAMN HIGH" % str(trawler_id))


    def cancel_unfinished_processes(self):
        for p_id in self.cluster_process_ids:
            try:
                subprocess.call(['scancel', str(p_id)])
            except subprocess.CalledProcessError, e:
                warnings.warn("Problem cancelling process " + str(p_id))
                print e.output

#
    def update_bash_submission_string(self):
        f = open(SLURM.TEMPLATE_FILE_SCRIPT_SUBMISSION, 'rb')
        self.bash_submission_template_string = f.read()
        f.close()
        self.bash_submission_template_string = self.bash_submission_template_string.replace(SLURM.TEMPLATE_QUEUE_NAME, self.partition_name)
        self.bash_submission_template_string = self.bash_submission_template_string.replace(SLURM.TEMPLATE_NUMBER_CORES, str(self.number_of_cores))
        self.bash_submission_template_string = self.bash_submission_template_string.replace(SLURM.TEMPLATE_NUMBER_MINUTES, str(self.time_requested_minutes))
        self.bash_submission_template_string = self.bash_submission_template_string.replace(SLURM.TEMPLATE_MEMORY_MB, str(self.memory_requested_MB))


class normal(Dispatcher):
    id_string = "normal"
    TEMP_FILE_STORAGE_DIRECTORY = "./TEMP/"
    def __init__(self, *args):
        super(normal, self).__init__()

    def __initiate_bash_shell_command__(self, ID_number):
        output = "python " + self.python_filename(ID_number)
        return output

    def __start_process__(self, ID_number):
        os.system(self.__initiate_bash_shell_command__(ID_number) + " &")
        return 0

    def __start_subprocess_trawler__(self, number):
        f = open(Dispatcher.TEMPLATE_FILE_PYTHON_TRAWLER, "rb")
        python_file_text = f.read()
        f.close()
        python_file_text = python_file_text.replace(SLURM.TEMPLATE_NUMBER, str(number))
        python_file_text = python_file_text.replace(SLURM.TEMPLATE_DIRECTORY_NAME, self.file_directory())

        trawler_id = "d" + str(self.dispatcher_id) + "_T" + str(number)

        python_filename = self.file_directory() + trawler_id + ".py"
        python_file = open(python_filename, "wb")
        python_file.write(python_file_text)
        python_file.close()
        os.system("python %s &" % python_filename)



dictionary_of_dispatcher_classes = {SLURM.id_string : SLURM, normal.id_string : normal}

def return_appropriate_dispatcher_object(dispatcher_id_string):
    return dictionary_of_dispatcher_classes[dispatcher_id_string]
