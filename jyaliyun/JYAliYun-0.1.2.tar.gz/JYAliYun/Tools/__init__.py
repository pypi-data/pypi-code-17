#! /usr/bin/env python
# coding: utf-8

import xml.dom.minidom

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
