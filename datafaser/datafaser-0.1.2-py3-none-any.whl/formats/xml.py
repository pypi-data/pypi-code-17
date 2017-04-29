import xml.etree.ElementTree as ET

help_topic = 'XML data representation'
help_text = '''
Each XML element is represented as a map with only one key, the element name,
pointing to a map with up to two optional keys:
  - 'attributes' points to a map containing the XML element's attributes
  - 'content' points to a list of strings and XML element representations
    in same order as in the XML inside the element.

For instance, XML

    <rootNode attr="value">
      text before subnode
      <subNode/>
      text after subnode
    </rootNode>

is represented as

    rootNode:
      attributes:
        attr: value
      content:
      - text before subnode
      - subNode: {}
      - text after subnode
'''


def read(stream):
    stream_content = ''.join(stream.read())
    root_element = ET.fromstring(stream_content)
    return element_to_structure(root_element)


def write(data, stream):
    root_element = structure_to_element(data)
    xml_string = ET.tostring(root_element, encoding='unicode')
    stream.write(xml_string)
    stream.write('\n')


def element_to_structure(element):
    if isinstance(element, ET.Element):
        content = []
        if element.text:
            content.append(element.text)
        for subelement in element:
            content.append(element_to_structure(subelement))
            if subelement.tail:
                content.append(subelement.tail)

        tag = {}
        if content:
           tag['content'] = content
        if element.attrib:
           tag['attributes'] = element.attrib

        return {
            element.tag: tag
        }
    else:
        return element


def structure_to_element(data_dict):
    builder = ET.TreeBuilder()
    build_xml(data_dict, builder)
    return builder.close()


def build_xml(data_dict, builder):
    tag_name = list(data_dict.keys())[0]
    tag = data_dict[tag_name]
    if 'attributes' in tag:
        attributes = tag['attributes']
    else:
        attributes = {}

    builder.start(tag_name, attributes)

    if 'content' in tag:
        for item in tag['content']:
            if isinstance(item, dict):
                structure_to_element(item, builder)
            else:
                builder.data(item)

    builder.end(tag_name)

