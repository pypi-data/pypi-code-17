# -*- coding: utf-8 -*-
import sys
from uuid import uuid4

MAX_SIZE = 128000
STAMP_SIZE = 70
STAMP_LENGTH = 40
UUID_LENGTH = 36
NEEDED_SIZE = MAX_SIZE - STAMP_SIZE
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

        if(index > len(self)):
            self.append(message)
        else:
            self.insert(index, message)

    def get_message(self):
        if self.message_segments == len(self) - 1:  # started from 0
            return "".join(self)


def segment_message(message):
    size = sys.getsizeof(message)
    message_uuid = str(uuid4())
    if size < MAX_SIZE:
        yield message
    else:
        segment_count = 0
        while True:
            stamp = message_uuid + "|" + str(segment_count).zfill(2) + "|"

            if not message:
                # all segements had been sent. Send  only the uuid and the number of segments
                yield stamp
                break
            for i in range(0, len(message) - 1):
                size = sys.getsizeof(message[0:i])
                next_size = sys.getsizeof(message[0:i + 1])
                if next_size > NEEDED_SIZE:
                    segment_count += 1
                    yield stamp + message[:i]
                    message = message[i:]
                    break
                if i + 1 == len(message) - 1:
                    # reached the end of message
                    yield stamp + message
                    message = None
                    break


def get_message(message):
    if _check_for_stamp(message):
        uuid = message[:UUID_LENGTH]
        message = message[UUID_LENGTH:]
        MESSAGE_DICT.setdefault(uuid, _Segments()).add(message)
        return MESSAGE_DICT[uuid].get_message()
    else:
        return message

    # check for message completion


def _check_for_stamp(message):
    # shallow check
    if len(message) < 40:
        return False
    else:
        # maybe a regex ? but I really hate regex
        has_seg_index = message[:STAMP_LENGTH][-4:].count("|") == 2
        has_uuid = message[:UUID_LENGTH].count("-") == 4  # yeah, i know, it does not need to be bulletproof
        return has_seg_index and has_uuid
