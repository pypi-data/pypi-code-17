# import threading
#
# import _thread
# import schedule
# import time
# from datetime import datetime, timedelta
#
# from .utils import start_schedule_thread, tasks_email_schedule, project_deadline_schedule
#
#
# def p():
#     print('yo', file=open('yo', 'a'))
#     # tasks_email_schedule()
#     # project_deadline_schedule()
#
#
# print('starting scheduler within users.__init__ ....')
# schedule.every().day.do(p)
#
#
# def run_schedule():
#     while len(schedule.jobs) > 0:
#         schedule.run_pending()
#         time.sleep(72000)
#
#
# _thread.start_new_thread(run_schedule, ())
