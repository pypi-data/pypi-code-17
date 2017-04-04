# -*- coding: utf-8 -*-
import sys
import math
from uuid import uuid4

MAX_SIZE = 128000
STAMP_SIZE = 70
STAMP_LENGTH = 40
UUID_LENGTH = 36
BUFFER = 50
NEEDED_SIZE = MAX_SIZE - STAMP_SIZE - BUFFER
MESSAGE_DICT = {}


class _Segments(list):
    message_segments = -1

    def add(self, item):
        index = int(item[:4].replace("|", ""))
        if(len(item) == 4):
            # wrapper message
            self.message_segments = index
            return
        message = item[4:]
        if index == 0:
            # 2 cases: one when the list is empty and one when it's not
            if not len(self):
                self.append(message)
            else:
                self[index] = message
        else:
            # check to see if extend is required
            length_required = index + 1
            if len(self) < length_required:
                diff = length_required - len(self)
                self.extend([None] * diff)
            self[index] = message

    def get_message(self):
        if self.message_segments == len(self) - 1:  # started from 0
            return "".join(self)


def segment_message(message):
    if not type(message) == str:
        # we can say that we are covered by size
        # but is nice to be guarded in case of a big object arrives
        raise Exception("Bad input, only strings accepted.")

    size = sys.getsizeof(message)
    message_uuid = str(uuid4())

    if size < MAX_SIZE:
        yield message
    else:
        needed_segments = float("{0:.02f}".format(size / float(NEEDED_SIZE)))
        full_segments = int(needed_segments)
        trailing = needed_segments - full_segments > 0

        # we extract 1 from needed_segments because 0 is counted
        last_segment_index = int(math.ceil(needed_segments) - 1)

        # send the stamp first to tell how much to expect. This will also be the last index that is sent
        # order arrival is not important actually
        stamp = message_uuid + "|" + str(last_segment_index).zfill(2) + "|"
        yield stamp

        for i in range(0, full_segments):
            stamp = message_uuid + "|" + str(i).zfill(2) + "|"
            yield stamp + message[:NEEDED_SIZE]
            message = message[NEEDED_SIZE:]

        if trailing:
            # send the last part
            stamp = message_uuid + "|" + str(last_segment_index).zfill(2) + "|"
            yield stamp + message


def get_message(message):
    global MESSAGE_DICT
    if _check_for_stamp(message):
        uuid = message[:UUID_LENGTH]
        message = message[UUID_LENGTH:]
        MESSAGE_DICT.setdefault(uuid, _Segments()).add(message)
        full_msg = MESSAGE_DICT[uuid].get_message()
        if full_msg:
            # delete the entry in the dict
            del MESSAGE_DICT[uuid]
        return full_msg
    else:
        return message


def _check_for_stamp(message):
    # shallow check
    if len(message) < 40:
        return False
    else:
        # maybe a regex ? but I really hate regex
        has_seg_index = message[:STAMP_LENGTH][-4:].count("|") == 2
        has_uuid = message[:UUID_LENGTH].count("-") == 4  # yeah, i know, it does not need to be bulletproof
        return has_seg_index and has_uuid
