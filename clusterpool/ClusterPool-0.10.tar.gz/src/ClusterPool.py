# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:05:52 2015

@author: joseph
"""

import time
import math

import numpy as np

from memory_profiler import memory_usage

import warnings

import Dispatcher
import Trawler

from os.path import expanduser



class Pool(object):
    memory_test_interval_seconds = 10
    target_process_time_minutes = 60

    MAX_CHECK_STATUS_LOOPS = 1000000
    timeout_time_s = 1 * 60 * 60 #1 hours times 60 minutes per hour times 60 seconds per minute
    TARGET_PROCESS_TIMES_MINUTES = 30.0


    MINIMUM_NUMBER_TRAWLERS = 10

    def __init__(self, maximum_number_of_jobs_running = -1, cluster_dispatcher_type = "SLURM"):
        "initialize a ClusterPool.Pool object to work on a specific cluster architecture"
        self.maximum_number_of_jobs_running = maximum_number_of_jobs_running
        self.cluster_dispatcher_type = cluster_dispatcher_type


    def map(self, function_to_apply, list_of_objects_to_calculate, index_of_slowest_calculation = -1, time_multiplier_worst_case = 6.0, memory_multiplier_worst_case = 1.2):
        "Use the cluster pool to map a function called calculate() on every member of the supplied list"

        self.list_of_objects_to_calculate = list_of_objects_to_calculate

        self.slowest_calculation = self.list_of_objects_to_calculate[index_of_slowest_calculation]

        self.my_function_to_apply = function_to_apply

        print "testing time and memory requirements..."
        self.slowest_calculation_completed = None

        start_time = time.time()
        self.slowest_calculation_completed = self.slowest_calculation.calculate()
        self.slowest_time_elapsed_s = time.time() - start_time
        process_completion_time_to_request_minutes = ( time_multiplier_worst_case * self.slowest_time_elapsed_s ) / 60.0
        process_memory_to_request_MB = memory_multiplier_worst_case * self.peak_memory_usage_megabytes()

        number_of_processes_per_trawler = int(math.ceil(Pool.TARGET_PROCESS_TIMES_MINUTES / process_completion_time_to_request_minutes))
        number_of_trawlers_to_create = int(math.ceil(float(len(list_of_objects_to_calculate) / number_of_processes_per_trawler)))
        number_of_trawlers_to_create = max([number_of_trawlers_to_create, Pool.MINIMUM_NUMBER_TRAWLERS])

        print "done!  child processes will request %s MB of RAM and %s minuters per core" % (str(process_memory_to_request_MB), str(process_completion_time_to_request_minutes)  )

        print "creating dispatcher"
        my_dispatcher = Dispatcher.return_appropriate_dispatcher_object(self.cluster_dispatcher_type)(process_completion_time_to_request_minutes, process_memory_to_request_MB)

        process_id_to_list_index_dict = {}
        unfinished_process_ids = []

        calculated_objects = []
        print("creating saved objects")
        for i, obj in enumerate(list_of_objects_to_calculate):
            calculated_objects.append(None)
            if i == index_of_slowest_calculation or i == (index_of_slowest_calculation + len(self.list_of_objects_to_calculate)):
                continue
            new_id = my_dispatcher.save_python_object_file_return_id(obj)
            process_id_to_list_index_dict[new_id] = i
            unfinished_process_ids.append(new_id)

        calculated_objects[index_of_slowest_calculation] = self.slowest_calculation_completed

        print("Spawning Trawlers")
        my_dispatcher.start_subprocess_trawlers(number_of_trawlers_to_create)

        myTrawler = Trawler.Trawler(my_dispatcher.file_directory(), number=-1)

        total_completed_calculations = 1
        loop_count = 0

        time.sleep(5)
        print("checking for finished calculations...")
        while len(unfinished_process_ids) > 0:
            try:
                myTrawler.find_and_complete_calculation()
            except Trawler.noMoreFilesToCalculate:
                pass

            loop_count = loop_count + 1

            #check for completed processes
            for process_id in unfinished_process_ids:
                try:
                    calc_obj = my_dispatcher.return_calculated_object(process_id)
                    calculated_objects[process_id_to_list_index_dict[process_id]] = calc_obj
                    unfinished_process_ids.remove(process_id)
                    my_dispatcher.delete_all_temp_files(process_id)

                    total_completed_calculations += 1
                    print("%i finished!" % total_completed_calculations)
                    continue

                except:

                    continue

        my_dispatcher.kill_dispatcher()
        return calculated_objects


    def peak_memory_usage_megabytes(self):
        """Memory usage of the current process in kilobytes."""
        status = None
        result = {'peak': 0, 'rss': 0}
        try:
            # This will only work on systems with a /proc file system
            # (like Linux).
            status = open('/proc/self/status')
            for line in status:
                parts = line.split()
                key = parts[0][2:-1].lower()
                if key in result:
                    result[key] = int(parts[1])
        except IOError:
            mem_usage_MB_history = memory_usage(-1, interval=self.slowest_time_elapsed_s/100.0, timeout=self.slowest_time_elapsed_s)
            return np.max(mem_usage_MB_history)
        finally:
            if status is not None:
                status.close()
        return float(result['peak'] ) / 1024.0

    def close(self):
        pass
