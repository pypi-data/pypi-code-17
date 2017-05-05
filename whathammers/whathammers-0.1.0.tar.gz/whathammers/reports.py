from collections import Counter
from itertools import groupby
from .utils import (
    aligned_labels, human_readable,
    readable_microseconds, slice_data
)


def top_values_by_hits(field, description, data, count):
    output = []
    output.append('Top %d %s by hits' % (count, description))
    output.append('-' * len(output[0]))

    value_counter = Counter([l.get(field, None) for l in data])
    table = []
    for value, hits in value_counter.most_common(count):
        value = human_readable(field, value)
        table.append((
            '%s:' % str(value),
            '%d hits (%.2f%% of total)' % (
                hits, 100.0*hits/len(data)
            )
        ))
    output = output + aligned_labels(table)
    return output


def hits_by_slice(field, description, data, count):
    output = []
    output.append('%s by hits, %d slices' % (description, count))
    output.append('-' * len(output[0]))

    slices = slice_data(field, data, count)

    max_hits = 0
    slice_hits = []
    for label, data in slices:
        if len(data) > max_hits:
            max_hits = len(data)
        slice_hits.append((label, len(data)))

    table = []
    for label, hits in slice_hits:
        table.append((
            '%s:' % label,
            '%s (%d hits)' % (
                '-' * ((40 * hits) // max_hits),
                hits
            )
        ))

    output = output + aligned_labels(table)
    return output


def top_values_by_total_time(field, description, data, count):
    output = []
    output.append('Top %d %s by total time' % (count, description))
    output.append('-' * len(output[0]))

    sorted_by_field = sorted(data, key=lambda e: e.get(field, None))
    grouped_by_field = groupby(
        sorted_by_field, lambda e: e.get(field, None)
    )
    time_by_value = {}
    total_time = 0
    for value, items in grouped_by_field:
        value_time = sum([int(e['time_us']) for e in items])
        total_time = total_time + value_time
        time_by_value[value] = value_time

    time_counter = Counter(time_by_value)
    table = []
    for value, time in time_counter.most_common(count):
        value = human_readable(field, value)
        table.append((
            '%s:' % str(value),
            '%s (%.2f%% of total)' % (
                readable_microseconds(time), 100 * float(time)/total_time
            )
        ))
    output = output + aligned_labels(table)
    return output


def time_by_slice(field, description, data, count):
    output = []
    output.append('%s by total time, %d slices' % (description, count))
    output.append('-' * len(output[0]))

    slices = slice_data(field, data, count)

    max_time = 0
    slice_times = []
    for label, data in slices:
        slice_time = sum([int(e['time_us']) for e in data])
        if slice_time > max_time:
            max_time = slice_time
        slice_times.append((label, slice_time))

    table = []
    for label, time in slice_times:
        table.append((
            '%s:' % label,
            '%s (%s)' % (
                '-' * ((40 * time) // max_time),
                readable_microseconds(time)
            )
        ))

    output = output + aligned_labels(table)
    return output


def top_values_by_time_per_hit(field, description, data, count):
    output = []
    output.append('Top %d %s by time per hit' % (count, description))
    output.append('-' * len(output[0]))

    sorted_by_field = sorted(data, key=lambda e: e.get(field, None))
    grouped_by_field = groupby(
        sorted_by_field, lambda e: e.get(field, None)
    )
    time_by_value = {}
    hits_by_value = {}
    total_time = 0
    for value, items in grouped_by_field:
        value_time = 0
        value_hits_count = 0
        for item in items:
            value_time = value_time + int(item['time_us'])
            value_hits_count = value_hits_count + 1
        total_time = total_time + value_time
        time_by_value[value] = float(value_time) / float(value_hits_count)
        hits_by_value[value] = value_hits_count

    time_counter = Counter(time_by_value)
    average_time = float(total_time) / len(data)
    table = []
    for value, time in time_counter.most_common(count):
        value = human_readable(field, value)
        table.append((
            '%s:' % str(value),
            '%s per hit (%.2f x average, based on %d (%.2f%%) of %d hits)' % (
                readable_microseconds(time), float(time)/average_time,
                hits_by_value[value],
                100.0 * float(hits_by_value[value])/len(data),
                len(data)
            )
        ))
    output = output + aligned_labels(table)
    return output


def time_per_hit_by_slice(field, description, data, count):
    output = []
    output.append('%s by time per hit, %d slices' % (description, count))
    output.append('-' * len(output[0]))

    slices = slice_data(field, data, count)

    max_time = 0
    slice_times = []
    for label, data in slices:
        slice_time = sum([int(e['time_us']) for e in data])
        slice_hits = len(data)
        slice_time_per_hit = slice_time // slice_hits
        if slice_time_per_hit > max_time:
            max_time = slice_time_per_hit
        slice_times.append((label, slice_time_per_hit))

    table = []
    for label, time in slice_times:
        table.append((
            '%s:' % label,
            '%s (%s)' % (
                '-' * ((40 * time) // max_time),
                readable_microseconds(time)
            )
        ))

    output = output + aligned_labels(table)
    return output
