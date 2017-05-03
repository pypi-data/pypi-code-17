# ===========================================
# log_functions.py
#
# Log functions used to show/write log on display/file
#
# Written by Sajjad Ziyaei amiri  (04/12/2016)
# ===========================================

import time
import platform

class uvp_log(object):
    def __init__(self):
        self.write_to_file = True 
        self.show_on_screen = False
        self.linux_log_path = "/var/log/"
        self.windows_log_path = ""
        self.log_filename = "uvp.log"
        self.error_log_filename = "uvp-error.log"
        self.tag = "UVP"

        if "Windows" in platform.system() :
            self.logpath =  self.windows_log_path + self.log_filename
            self.errlogpath = self.windows_log_path + self.error_log_filename
        elif "Linux" in platform.system():
            self.logpath = self.linux_log_path + self.log_filename
            self.errlogpath = self.linux_log_path + self.error_log_filename
    
    # ======================================
    def set_write_to_file (self,a):
        self.write_to_file = a

    def set_show_on_screen (self,a):
        self.show_on_screen = a 

    def set_tag (self,a):
        self.tag = a

    def set_log_filename (self,a):
        self.log_filename = a 
        if "Windows" in platform.system() :
            self.logpath =  self.windows_log_path + self.log_filename
        elif "Linux" in platform.system():
            self.logpath = self.linux_log_path + self.log_filename     

    def set_error_log_filename (self,a):
        self.error_log_filename = a 
        if "Windows" in platform.system() :
            self.errlogpath = self.windows_log_path + self.error_log_filename
        elif "Linux" in platform.system():
            self.errlogpath = self.linux_log_path + self.error_log_filename       

    # ======================================
    def info (self,text):
        #print "UVP >> ", text
        log = time.strftime("%d/%m/%Y %H:%M:%S")+" >> "+self.tag+" >> INFO >> "+ text
        if self.write_to_file:
            self._write_log_to_file (log)
        if self.show_on_screen:
            print log
        
    def warning(self,text):
        #print "UVP >> **** WARNING **** " + text
        log = time.strftime("%d/%m/%Y %H:%M:%S")+" >> "+self.tag+" >> WARNING >> "+ text
        if self.write_to_file:
            self._write_log_to_file (log)
            self._write_error_to_file (log)
        if self.show_on_screen:
            print log

    def error(self, text):
        #print "UVP >> **** ERROR **** " + text
        log = time.strftime("%d/%m/%Y %H:%M:%S")+" >> "+self.tag+" >> ERROR >> "+ text
        if self.write_to_file:
            self._write_log_to_file (log)
            self._write_error_to_file (log)
        if self.show_on_screen:
            print log

    # ======================================        
    def _write_log_to_file(self,text):
        f = open(self.logpath,'a')
        f.write(text+"\n")
        f.close()

    def _write_error_to_file(self,text):
        f = open(self.errlogpath,'a')
        f.write(text+"\n")
        f.close()