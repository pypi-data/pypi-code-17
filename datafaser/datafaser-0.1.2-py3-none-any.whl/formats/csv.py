import csv


def read(stream):
    reader = csv.reader(stream)
    return [row for row in reader]


def write(data, stream):
    writer = csv.writer(stream)
    for row in data:
        writer.write(row)
