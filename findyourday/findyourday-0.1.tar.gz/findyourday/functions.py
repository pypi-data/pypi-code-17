""" This module gives the day of the week for a given date"""

import datetime
import re
import dateformatexceptions


weekdays_dict = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3:"Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}


def find_day():
    
    """ This function prints and returns the day of the week for a date typed by the user"""

    yourdate_object = None

    while yourdate_object is None:
        try:
            yourdate = raw_input(
                "Please input the date in the day/month/year format. e.g. 01/01/2017 \n")
            if re.match(r"[a-zA-Z]", yourdate):
                raise dateformatexceptions.IncludesStringError()
            
            if re.match(r".*\\.*", yourdate):
                raise dateformatexceptions.IncludesBackwardslashError

            yourdate_object = datetime.datetime.strptime(yourdate, "%d/%m/%Y")
            yourday = weekdays_dict[yourdate_object.weekday()]
            print "The day of the date ", yourdate, " is: \n", yourday

        except dateformatexceptions.IncludesStringError:
            print "Format error. Date should not include letters. \n"
        except dateformatexceptions.IncludesBackwardslashError:
            print "Format error. Date should follow 01/01/2017 format. Days, months, and years should be separated by forward slashes (/). Do not type backward slashes(\). \n"
        except ValueError:
            print "ValueError. Please follow the day/month/year format e.g. 01/01/2017 \n"

    return yourday

