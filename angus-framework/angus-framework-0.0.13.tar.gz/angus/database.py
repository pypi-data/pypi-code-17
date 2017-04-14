import base64
import datetime
import pytz
from dateutil.parser import parse as dparse

import os
import os.path
import logging
import json
import math
from collections import OrderedDict

import cv2

LOGGER = logging.getLogger("jobs_db")

SPEED_THRESHOLD = 200
SALESMAN_TIME = 10 # seconds
IS_FOCUS_THRESHOLD = 0.5

INTERESTED_TR_AGE = 3
INTERESTED_FOCUS_T = 1
INTERESTED_STOP_T = 3

PWD = os.path.dirname(__file__)

class FullEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

class Database(object):
    def __init__(self, max_size=10):
        self.data = OrderedDict()
        self.max_size = max_size
        self.center_zone = 0.18
        self.center_inc = 0.05

    def init_entry(self, key, ts):

        if len(self.data) >= self.max_size:
            self.data.popitem(last=False)

        entry = {
            "entity_id": key,
            "ts": ts,

            "creation_date": datetime.datetime.now(pytz.utc),
            "age": -1,
            "age-range": "",
            "gender": "?",
            "emotion": "neutral",
            "focus_center": 0,
            "start_ts": ts,
            "track_age": 0,

            "focus_start": ts,
            "focus_time": 0,

            "stop_start": ts,
            "stop_time": 0,
            "moving": False,
            "last_x": None,
            "last_y": None,
            "direction": None,
            "salesman": False,
            "population_category": None,
            "satisf_pos_count": 0,
            "satisf_neg_count": 0,
            "satisfaction_ratio": 0,
        }
        self.data[key] = entry

        return entry

    def update_category(self, entity):
        age = entity["age"]
        gender = entity["gender"]

        if age == -1 or gender == "?":
            return

        if age > 50:
            prefix = "Senior"
        else:
            prefix = "Young"

        entity["population_category"] = "{} {}".format(prefix, gender)


    def update(self, res, req_info, frame=None, notifications=None):
        events = res["events"]
        entities = res["entities"]
        ts = dparse(res["timestamp"])
        for key, val in entities.iteritems():

            # Initialize if new entity
            if key not in self.data:
                entity = self.init_entry(key, ts)
            else:
                entity = self.data[key]

            # Update last seen timestamp
            last_ts = entity["ts"]
            entity["ts"] = ts

            entity["track_age"] = (ts-entity["start_ts"]).total_seconds()

            # Compute focus center
            focus_center = entity["focus_center"]
            focus_before = focus_center > IS_FOCUS_THRESHOLD

            # height_offset = -0.2 # target lower than camera 0.5 ~ 30 degrees
            height_offset = 0.0
            # height_offset = 0.5 # target higher than camera
            yaw, pitch=val["gaze"]
            pitch-=height_offset

            if abs(yaw) < self.center_zone \
                and abs(pitch) < self.center_zone \
                and yaw!=0 \
                and pitch!=0 :
                focus_center += self.center_inc
            else:
                if yaw==0 and pitch==0:
                    focus_center -= self.center_inc
                else : focus_center -= self.center_inc
            focus_center = min(1, max(focus_center, 0))
            focus_after = focus_center > IS_FOCUS_THRESHOLD
            entity["focus_center"] = focus_center

            if focus_before and not focus_after:
                entity["focus_time"] += (ts-entity["focus_start"]).total_seconds()

            if not focus_before:
                entity["focus_start"] = ts

            # Compute stops
            last_x = entity["last_x"]
            last_y = entity["last_y"]
            moving_before = entity["moving"]
            x, y, dx, dy = map(int, val["face_roi"])
            entity["last_x"] = x
            entity["last_y"] = y

            if last_x is None or last_y is None:
                moving_after = False
            else:
                speed = math.sqrt((x-last_x)**2 + (y-last_y)**2) / (ts-last_ts).total_seconds()
                moving_after = speed > SPEED_THRESHOLD

            entity["moving"] = moving_after

            if not moving_before and moving_after:
                entity["stop_time"] += (ts-entity["stop_start"]).total_seconds()

            if moving_before:
                entity["stop_start"] = ts

            if entity["track_age"] > SALESMAN_TIME and not entity["salesman"]:
                entity["salesman"] = True
                if frame:
                    head = frame[y:y+dy, x:x+dx]
                    _, head = cv2.imencode(".jpg", head, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    head = base64.b64encode(head)
                    head = "data:image/jpg;base64,{}".format(head)
                    if notifications:
                        notifications.append({"msg": "Salesman needed !!!", "img": head})

        for event in events:
            entity_id = event["entity_id"]
            if not entity_id in self.data:
                continue

            entity = self.data[entity_id]
            key = event["key"]

            new_value = entities[entity_id][key]
            key_split = key.split("_")
            if key_split[0] == "emotion":
                entity[key_split[0]] = key_split[1]
                # Incrementing pos and neg satisfaction counter to Compute
                # a satisfaction ratio when track disappear
                if key_split[1] == "happiness" or key_split[1] == "surprise":
                    entity["satisf_pos_count"] += 1
                elif key_split[1] == "sadness" or key_split[1] == "anger":
                    entity["satisf_neg_count"] += 1
            elif key == "age":
                entity[key] = new_value
                confidence = entities[entity_id]["age_confidence"]
                margin = int((1-confidence)*5 + 1)
                entity["age-range"] = "{}-{}".format(new_value - margin, new_value + margin)
            elif event["type"] == "disappearance":
                entity["focus_time"] += (ts-entity["focus_start"]).total_seconds()
                direction = entities[entity_id]["direction"]
                entity["direction"] = direction
                if direction == "left":
                    entity["exit"] = 1
                elif direction == "right":
                    entity["enter"] = 1
                if not entity["moving"]:
                    entity["stop_time"] += (ts-entity["stop_start"]).total_seconds()
                    entity["stop_start"] = ts

                # Setting track as interested when some conditions are met
                if entity["track_age"] > INTERESTED_TR_AGE \
                    and entity["focus_time"] > INTERESTED_FOCUS_T \
                    and entity["stop_time"] > INTERESTED_STOP_T:
                    entity["interested"] = 1

                # This is to display a satisfaction ratio on a timeline in kibana
                if entity["satisf_pos_count"] + entity["satisf_neg_count"] > 0:
                    # Computing a satisfaction ratio between [0;1]
                    entity["satisfaction_ratio"] = entity["satisf_pos_count"]\
                    /float(entity["satisf_pos_count"] + entity["satisf_neg_count"])
                    # Scaling the satisfaction ratio to [-1;1]
                    entity["satisfaction_ratio"] = 2*entity["satisfaction_ratio"] - 1

            elif not "face" in key:
                entity[key] = str(new_value)
            if key == "age" or key == "gender":
                self.update_category(entity)

            txt = entity.copy()
            txt.update({
                "event_type": event["type"],
            })
            txt.update(req_info)

            LOGGER.info(json.dumps(txt, cls=FullEncoder))
