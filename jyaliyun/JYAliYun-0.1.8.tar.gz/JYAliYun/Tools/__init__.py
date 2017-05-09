#! /usr/bin/env python
# coding: utf-8

import os
import ConfigParser
import hmac
import hashlib
import base64
from datetime import datetime
import xml.dom.minidom
from JYAliYun import GMT_FORMAT

__author__ = 'ZhouHeng'

XMLNS = "http://www.gene.ac"


class ConvertObject(object):
    encoding = "utf-8"

    @staticmethod
    def decode(s):
        if isinstance(s, str):
            return s.decode(ConvertObject.encoding)
        return s

    @staticmethod
    def encode(s):
        if isinstance(s, unicode):
            return s.encode(ConvertObject.encoding)
        return s

    @staticmethod
    def dict_to_xml(tag_name, dict_data):
        tag_name = ConvertObject.decode(tag_name)
        doc = xml.dom.minidom.Document()
        root_node = doc.createElement(tag_name)
        root_node.setAttribute("xmlns", XMLNS)
        doc.appendChild(root_node)
        assert isinstance(dict_data, dict)
        for k, v in dict_data.items():
            key_node = doc.createElement(k)
            if isinstance(v, dict):
                for sub_k, sub_v in v.items():
                    sub_node = doc.createElement(sub_k)
                    sub_v = ConvertObject.decode(sub_v)
                    sub_node.appendChild(doc.createTextNode(sub_v))
                    key_node.appendChild(sub_node)
            else:
                v = ConvertObject.decode(v)
                key_node.appendChild(doc.createTextNode(v))
            root_node.appendChild(key_node)
        return doc.toxml("utf-8")


class ConfigManager(object):
    def __init__(self, **kwargs):
        self.section = kwargs.pop("section", None)
        if self.section is None:
            self.section = kwargs.pop("default_section", None)

        self.conf_path = kwargs.pop("conf_path", None)
        if self.conf_path is None:
            conf_dir = kwargs.pop("conf_dir", None)
            if isinstance(conf_dir, str) or isinstance(conf_dir, unicode):
                conf_name = kwargs.pop("conf_name", None)
                default_conf_name = kwargs.pop("default_conf_name", None)
                if conf_name is not None:
                    self.conf_path = os.path.join(conf_dir, conf_name)
                elif default_conf_name is not None:
                    self.conf_path = os.path.join(conf_dir, default_conf_name)
        if self.conf_path is None or self.section is None:
            self.ready = False
        else:
            self.config = ConfigParser.ConfigParser()
            self.config.read(self.conf_path)
            self.ready = self.config.has_section(self.section)

    def _get(self, option, option_type=None, default=None):
        if self.ready is False:
            return default
        if self.config.has_option(self.section, option) is False:
            return default
        if option_type is None:
            self.config.get(self.section, option)
        if option_type == int:
            return self.config.getint(self.section, option)
        elif option_type == bool:
            return self.config.getboolean(self.section, option)
        elif option_type == float:
            return self.config.getfloat(self.section, option)
        return self.config.get(self.section, option)

    def get(self, option, default=None):
        return self._get(option, default=default)

    def getboolean(self, option, default=None):
        return self._get(option, bool, default=default)

    def getint(self, option, default):
        return self._get(option, int, default=default)

    def getfloat(self, option, default):
        return self._get(option, float, default=default)

    def has_option(self, option):
        if self.ready is False:
            return False
        return self.config.has_option(self.section, option)


def ali_headers(access_key_id, access_key_secret, request_method, content_md5, content_type, headers, resource,
                **kwargs):
    request_time = datetime.utcnow().strftime(GMT_FORMAT)
    x_headers = dict()
    product = kwargs.pop("product", "")
    x_headers_key = "x-%s" % product.lower()
    if isinstance(headers, dict):
        for k, v in dict(headers).items():
            if k.startswith(x_headers_key):
                x_headers[k] = v
    else:
        headers = dict()
    if content_type is not None and len(content_type) > 0:
        headers["Content-Type"] = content_type
    signature = ali_signature(access_key_secret, request_method, content_md5, content_type, request_time, x_headers,
                              resource, **kwargs)

    headers["Authorization"] = product.upper() + " %s:%s" % (access_key_id, signature)
    headers["Date"] = request_time
    return headers


def ali_signature(access_key_secret, request_method, content_md5, content_type, request_time, x_headers, resource,
                  **kwargs):
    if content_md5 is None:
        content_md5 = ""
    if content_type is None:
        content_type = ""
    x_headers_s = ""
    if x_headers is not None:
        if type(x_headers) == unicode:
            x_headers_s = x_headers
        elif type(x_headers) == dict:
            for key in sorted(x_headers.keys()):
                x_headers_s += key.lower() + ":" + x_headers[key] + "\n"
    msg = "%s\n%s\n%s\n%s\n%s%s" % (request_method, content_md5, content_type, request_time, x_headers_s, resource)
    if "print_sign_msg" in kwargs:
        print(msg)
    h = hmac.new(access_key_secret, msg, hashlib.sha1)
    signature = base64.b64encode(h.digest())
    return signature


if __name__ == "__main__":
    config_man = ConfigManager(conf_dir="/data/Web2/conf", conf_name="mns.conf", section="Account")
    print config_man.get("access_key_id")
