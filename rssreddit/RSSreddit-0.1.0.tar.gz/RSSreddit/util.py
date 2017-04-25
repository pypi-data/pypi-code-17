"""Helper functions for rssreddit."""

import re
import requests
from xml.etree import ElementTree


def getXML(url):
    """
    Get XML from url.

    Args:
        url: URL of the RSS.

    Returns:
        An Element which is the root of the XML tree.
    """
    try:
        response = requests.get(url, headers={'User-agent': 'RSSreddit'})
        if response.status_code == 200:
            xmlelement = ElementTree.fromstring(response.content)
            return xmlelement
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("Error: ", e)


def tag_name(tag):
    """Strip namespace and return tag."""
    return re.findall(r'}(\w+)', tag.tag)[0] or None


def recurseXML(element):
    """Convert XML to JSON."""
    data = {}
    for elem in element:
        item = tag_name(elem)
        if elem.attrib and type(elem.text) is str:
            data[item] = elem.attrib
            data[item].update({item: elem.text})
        elif type(elem.text) is str:
            data[item] = elem.text
        elif elem.attrib:
            if item in data:
                data[item].append(elem.attrib)
            else:
                data[item] = [elem.attrib]
        else:
            if item in data:
                data[item].append(recurseXML(elem))
            else:
                data[item] = [recurseXML(elem)]
    return data
