from adb_functions import *
phone = uvp_phone()

phone.uvp_log.set_write_to_file(True)
phone.set_log_on_screen (True)
phone.uvp_log.tag = "NEW"

phone.uvp_log.info("mu log here ! ")
phone.set_Phone_IP ("10.100.200.10")
phone.adb_disconnect()
phone.adb_connect()
phone.clear_history()
phone.adb_disconnect()


#from log_functions import *
#log = uvp_log ()
#log.set_write_to_file(False)
#log.set_show_on_screen(False)
#import time
#log.info (time.strftime("%H:%M:%S"))
