import socket
from datetime import datetime


def aligned_labels(values):
    """ Given a list of tuples (label, value) return a list of lines
        as "label value" such that all the values are aligned.
    """
    output = []
    length = max([len(v[0]) for v in values])
    the_format = '{:>' + str(length) + '} {}'
    for line in values:
        output.append(the_format.format(line[0], line[1]))
    return output


def field_description(field):
    """ Given an apache_log_parser field
        (see https://github.com/rory/apache-log-parser)
        return a description of the field, or at worst
        the name of the field back
    """
    descriptions = {
        'remote_host': 'remote host',
        'request_header_user_agent': 'user agent'
    }
    if field in descriptions:
        return descriptions[field]
    else:
        return field


def human_readable(field_name, value):
    """ Given a field_name and a value
        return the human readable version
        of the value (eg. truncate long
        user agent, resolve, IP addresses,
        etc.
    """
    if field_name == 'remote_host':
        try:
            reverse = socket.gethostbyaddr(value)
            return reverse[0]
        except socket.herror:
            return value
    elif field_name == 'request_header_user_agent':
        if len(value) > 40:
            value = value[:37] + '...'
        return value
    return value


def readable_microseconds(value):
    if value > 1000000:
        return "%.2f seconds" % (float(value)/1000000)
    elif value > 1000:
        return "%.2f miliseconds" % (float(value)/1000)
    else:
        return "%d microseconds" % value


def is_continuous(field_name):
    """ Given an apache log_parser field name,
        return TRUE if that field is continuous
    """
    return field_name == 'time_received'


def slice_data(field_name, data, count):
    if field_name != 'time_received':
        raise Exception('Do not know how to slice by %s' % field_name)

    sorted_data = sorted(data, key=lambda k: k['time_received_datetimeobj'])
    first = sorted_data[0]['time_received_datetimeobj']
    last = sorted_data[-1]['time_received_datetimeobj']
    slice_length = (last - first)/count

    slices = []
    current_slice = []
    last_time = first
    label_fmt = '%Y-%m-%d %H:%M:%S'
    for row in data:
        if row['time_received_datetimeobj'] - last_time > slice_length:
            slices.append((
                datetime.strftime(last_time, label_fmt), current_slice)
            )
            current_slice = []
            last_time = last_time + slice_length
        current_slice.append(row)
    slices.append((datetime.strftime(last_time, label_fmt), current_slice))
    return slices
