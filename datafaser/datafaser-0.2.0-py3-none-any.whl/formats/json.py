import json


def read(stream):
    return json.load(stream)


def write(data, stream):
    json.dump(data, stream, indent=4, ensure_ascii=False)
    stream.write('\n')
