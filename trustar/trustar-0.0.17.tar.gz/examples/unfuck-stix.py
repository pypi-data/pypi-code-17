from lxml import etree
import untangle
import xmltodict

file="/Users/croblee/Downloads/stix_offender.xml"


def etree_to_dict(t):
    d = {t.tag : map(etree_to_dict, t.iterchildren())}
    d.update(('@' + k, v) for k, v in t.attrib.iteritems())
    d['text'] = t.text
    return d


parser = etree.XMLParser(ns_clean=True, recover=True)
tree = etree.parse(file, parser)

td=etree_to_dict(tree.getroot())

doc = xmltodict.parse(file)



# print(td)
# root = etree.getroot()
# print(ET.tostring(root.find('test')))



