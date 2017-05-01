from datetime import datetime

from dateutil import parser as dt_parser
import pytz


def str_start_to_str_runtime(started):
  delta = datetime.now(pytz.utc) - dt_parser.parse(started)

  # Truncate the integers
  days = int(delta.days)
  hours = int(delta.seconds / 3600)
  minutes = int((delta.seconds % 3600) / 60)
  seconds = int(delta.seconds % 60)

  running = ''

  if days:
    running += '{} day'.format(days)
    running += 's ' if days > 1 else ' '

  if hours:
    running += '{} hour'.format(hours)
    running += 's ' if hours > 1 else ' '

  if minutes:
    running += '{} minute'.format(minutes)
    running += 's ' if minutes > 1 else ' '

  running += '{} seconds'.format(seconds)

  return running
