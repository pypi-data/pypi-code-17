import pandas as pd
from dateutil import parser

def is_dict_in_timerange(start_dt, end_dt, gcal_dict):
    '''
    inputs: start_dt and end_dt (datetime) as well as gcal_dict (google calendar dict)
        from get_entity_busy_status
    outputs: 0 or 1 whether or not start_dt and end_dt intersect any busy time
        in the google calendar dict
    '''
    busy_list = []

    for key, cal_dict in gcal_dict['calendars'].iteritems():
        busy_temp = 0
        busy_dict = cal_dict['busy']
        if not busy_dict:
            if 'errors' in cal_dict:
                busy_list.append([key, 1])
                continue
            else:
                busy_list.append([key, 0])
                continue
        else:
#             iterate through the busy_dict and check if busy times intersect
            for busy in busy_dict:
#                 remove the US/Central offset tzinfo
                temp_start_dt = parser.parse(busy['start']).replace(tzinfo=None)
                temp_end_dt = parser.parse(busy['end']).replace(tzinfo=None)
                if (start_dt <= temp_start_dt < end_dt) or (start_dt < temp_end_dt <= end_dt) \
                    or (temp_start_dt <= start_dt and temp_end_dt >= end_dt):
                    busy_temp = 1

        busy_list.append([key, busy_temp])

    df_busy = pd.DataFrame(busy_list, columns=['subject', 'status'])
    df_busy['start'] = start_dt
    df_busy['end'] = end_dt

    return df_busy
