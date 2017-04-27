import sys


def get_location():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    location = '%s %s' %(exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno)
    return location