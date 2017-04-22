#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author: Pablo Saavedra
# Maintainer: Pablo Saavedra
# Contact: psaavedra at igalia.com

import logging
import sys
import ConfigParser
import csv
import requests


def get_default_settings():
    settings = {}
    settings["global"] = {
        "loglevel": 10,
        "logfile": "/dev/stdout",
        "url": "http:/u/localhost/",
        "dryrun": False
    }
    settings["auth"] = {
        "type": "http_basic",
        "username": "user",
        "password": "password",
    }
    return settings


def set_setting(settings, s, k, v):
    if s == "global":
        if k == "loglevel":
            settings[s][k] = int(v)
        elif k == "dryrun":
            if v.lower() in ("1", "true"):
                settings[s][k] = True
            else:
                settings[s][k] = False
        else:
            settings[s][k] = v

    else:
        if s.startswith("org__"):
            org_name = s[5:]
            if org_name not in settings["org"]:
                settings["org"][org_name] = {}
            if k.startswith("team__"):
                ldap_name = k[6:]
                settings["org"][org_name][ldap_name] = v
        else:
            settings[s][k] = v


def setup(conffile, settings):
    cfg = ConfigParser.ConfigParser()
    cfg.read(conffile)
    for s in cfg.sections():
        for k, v in cfg.items(s):
            set_setting(settings, s, k, v)


def debug_conffile(settings, logger):
    for s in settings.keys():
        for k in settings[s].keys():
            key = "%s.%s" % (s, k)
            value = settings[s][k]
            if k.find("passw") == -1:
                logger.debug("Configuration setting - %s: %s" % (key, value))


def create_logger(settings):
    hdlr = logging.FileHandler(settings["global"]["logfile"])
    hdlr.setFormatter(logging.Formatter('%(levelname)s %(asctime)s %(message)s'))
    logger = logging.getLogger('twiki')
    logger.addHandler(hdlr)
    logger.setLevel(settings["global"]["loglevel"])
    logger.debug("Default encoding: %s" % sys.getdefaultencoding())
    debug_conffile(settings, logger)
    return logger


def get_logger():
    return logging.getLogger('twiki')


def get_2_columns_csv(csvfile):
    with open(csvfile, 'rb') as csvfile_d:
        reader = csv.reader(csvfile_d)
        for row in reader:
            if len(row) < 1:
                yield (row[0], "")
            else:
                yield (row[0], row[1])


class Twiki():
    def __init__(self, settings):
        self.logger = create_logger(settings)
        self.settings = settings

    def do_get_action(self, str_, auth):
        self.logger.debug(str_)
        r = requests.get(str_, auth=auth)
        return r

    def do_post_action(self, str_, auth, data={}):
        self.logger.debug(str_)
        r = requests.post(str_,
                          data=data,
                          auth=auth)
        return r

    def get_topics(self, web):
        auth = (self.settings["auth"]["username"],
                self.settings["auth"]["password"])
        url = self.settings["global"]["url"]
        str_ = '%s/bin/view/%s/WebTopicList' % (url, web)
        r = self.do_get_action(str_, auth)
        self.logger.info("Action %s - %s: %s" % ("gettopics",
                         web, r.status_code))
        res = []
        for l in r.content.split("\n"):
            if l.find("twikiLink") > -1:
                r = l.split('href="/twiki/bin/view/')[1].split('"')[0]
                res.append(r)
        return res

    def move_topic(self, topic, parent_topic):
        auth = (self.settings["auth"]["username"],
                self.settings["auth"]["password"])
        url = self.settings["global"]["url"]
        str_ = '%s/bin/save/%s?%s=%s' % (url,
                                         topic,
                                         "topicparent",
                                         parent_topic)
        r = self.do_get_action(str_, auth)
        self.logger.info("Action %s - %s - %s: %s" % ("topicparent", topic,
                         parent_topic, r.status_code))

    def rename_topic(self, topic, new_topic):
        auth = (self.settings["auth"]["username"],
                self.settings["auth"]["password"])
        url = self.settings["global"]["url"]
        str_ = '%s/bin/rename/%s' % (url, topic)

        # Getting the list of topics to be updated with the new reference to
        # the content
        r = self.do_get_action(str_, auth)
        referring_topics = []
        for l in r.content.split("\n"):
            if l.find('class="twikiTopRow"') > -1:
                for ll in l.split("<input"):
                    if ll.find('twikiCheckBox') > -1:
                        r = ll.split('value="')[1].split('"')[0]
                        referring_topics.append(r)

        new_web = new_topic.split("/")[0]
        new_topic_ = "/".join(new_topic.split("/")[1:])
        data = {}
        data["newweb"] = new_web
        data["newtopic"] = new_topic_
        data["nonwikiword"] = "on"
        data["referring_topics"] = referring_topics
        r = self.do_post_action(str_, auth, data)
        self.logger.info("Action %s - %s - %s: %s %s" % ("renametopic", topic,
                         new_topic, r.status_code, r.content))
        self.logger.debug("Result %s : %s" % ("renametopic", r.content))
