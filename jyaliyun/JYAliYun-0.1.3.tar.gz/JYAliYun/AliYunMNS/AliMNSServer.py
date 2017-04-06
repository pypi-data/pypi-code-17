#! /usr/bin/env python
# coding: utf-8

import os
import ConfigParser

from JYAliYun import AliYUN_DOMAIN_NAME
from JYAliYun.AliYunAccount import RAMAccount
from JYAliYun.AliYunObject import ObjectManager
from JYAliYun.AliYunMNS.AliMNSTopics import MNSTopicsManager

__author__ = 'ZhouHeng'


class MNSServerManager(ObjectManager):
    """
    配置文件格式
    [MNS]
    account_id: 1530531001163833
    region: beijing
    internal: false
    """

    def __init__(self, account, **kwargs):
        assert isinstance(account, RAMAccount)
        super(MNSServerManager, self).__init__()
        conf_path = kwargs.pop("conf_path", None)
        conf_dir = kwargs.pop("conf_dir", None)
        if conf_path is not None:
            section = kwargs.pop("section", "MNS")
            self._load_conf(conf_path, section)
        elif conf_dir is not None:
            conf_name = kwargs.pop("conf_name", "mns.conf")
            conf_path = os.path.join(conf_dir, conf_name)
            section = kwargs.pop("section", "MNS")
            self._load_conf(conf_path, section)
        else:
            self.account_id = kwargs["account_id"]
            self.region = kwargs["region"]
            self.internal = kwargs.pop("internal", False)
        account.assign_access_key(self)

    def _load_conf(self, conf_path, section):
        config = ConfigParser.ConfigParser()
        config.read(conf_path)
        self.account_id = config.get(section, "account_id")
        self.region = config.get(section, "region")
        self.internal = config.getboolean(section, "internal")

    def get_server_url(self):
        if self.server_url is not None:
            return self.server_url
        if self.internal is True:
            protocol = "http"
            region_ext = "-internal"
        else:
            protocol = "http"
            region_ext = ""
        self.server_url = "%s://%s.mns.cn-%s%s.%s" % (protocol, self.account_id, self.region, region_ext,
                                                      AliYUN_DOMAIN_NAME)
        return self.server_url

    def get_topic(self, topic_name):
        mns_topic = MNSTopicsManager(topic_name)
        mns_topic.set_server_url(self.get_server_url())
        mns_topic.set_access_key_id(self.access_key_id)
        mns_topic.set_access_key_secret(self.access_key_secret)
        return mns_topic
