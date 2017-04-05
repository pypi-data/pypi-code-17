"""
Created on Wed May 20 15:20:35 2015

@author: joseph
"""
import cPickle as pickle
import sys
import os
import random
import glob

class noMoreFilesToCalculate(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class Trawler(object):

    def __init__(self, file_directory, number = 0, function = None):
        sys.path.append(os.getcwd())
        self.myDirectory = file_directory
        self.myNumber = number

        if function == None:
            self.myFunction = lambda x: x.calculate()

        self.number_of_completed_calculations = 0

    def run(self):
        while True:
            try:
                self.find_and_complete_calculation()
                self.number_of_completed_calculations = self.number_of_completed_calculations + 1
            except noMoreFilesToCalculate:
                print "We done here! This trawler(#%s) is OUTTA HERE and I did %s calculations all by myself! --- *MIC DROP*" % (str(self.myNumber), str(self.number_of_completed_calculations))
                break

    def find_and_complete_calculation(self):
        found_obj = False
        while not found_obj:
#            print "checking directory for uncalculated files"
            #This should throw an exception when there are no more uncalculated files...
            list_uncalculated = glob.glob(self.myDirectory + "*.uncalculated.pkl")
            if len(list_uncalculated) == 0:
                raise noMoreFilesToCalculate()
            for i in range(100):
                filename = random.choice(list_uncalculated)
                idNumber = filename.split(".")[-3].split("/")[-1]
                try:
                    #check to see if the id_number.working exists already and if it does, move along
                    working_mutex_filename = self.myDirectory + idNumber+ ".working"
                    fff = open(working_mutex_filename, 'r')
                    fff.close()
                except IOError:
                    #the system will throw an io error if #.working does not exist, which means we can calculate!
                    f = open(working_mutex_filename, 'w')
                    f.write("I'm workin' heeeeeeerre")
                    f.close()
                    try:
                        my_file_to_be_caculated =  open(filename, 'r')
                        found_obj = True
                        break
                    except IOError, e:
                        print "oops, rare collision happened!  Oh well.  Get on with your life.  Here's the message if you care:"
                        print e.message
                        continue




        my_object_to_be_caculated =  pickle.load(my_file_to_be_caculated)

        #CALCULATE!
        calculated_object = self.myFunction(my_object_to_be_caculated)

        #cleanup
        calculated_filename = filename.split(".")
        calculated_filename[-2] = "CALCULATED"
        calculated_filename = ".".join(calculated_filename)
        calculated_object_file = open(calculated_filename, 'w')
        pickle.dump(calculated_object, calculated_object_file)
        calculated_object_file.close()

        try:
            os.remove(filename)
            os.remove(working_mutex_filename)
        except:
            pass
