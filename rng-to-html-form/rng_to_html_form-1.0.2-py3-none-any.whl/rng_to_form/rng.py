from lxml import objectify
import collections
from itertools import chain
from lxml import etree as E


def tag_name(x):
    return x.tag.rsplit('}')[1]


class RNG(object):
    """
    Stuff related to relaxNg docs.
    """

    def etree_to_dict(self, t):
        attributes = {k: v for k, v in t.attrib.iteritems()}
        if t.text:
            attributes.update({"text": t.text})
        d = {tag_name(t): [[elem for elem in map(
            self.etree_to_dict, t.getchildren())], attributes]}
        return d

    def __init__(self, file=None, target=None, *args, **kwargs):
        """
        This is an init
        """
        self.optionals = []
        if file:
            self.relax_doc = E.parse(file)
            objectify.deannotate(self.relax_doc, cleanup_namespaces=True)
            self.root = self.relax_doc.getroot()
            self.structure = self.etree_to_dict(self.root)
            self.target = target

    def to_form(self):
        """ """
        tree = self.relax_doc
        definitionx = self.find_def(self.find_target_ref())
        results = collections.OrderedDict()

        names = []

        def get_cardinality_target(e):
            """In the wonderful format rng, when ther is a cardinality somewehere, elements are pushed one level deeper"""
            ref_list = e.findall(".//rng:ref", self.root.nsmap)
            target = None
            if len(ref_list):
                ref = ref_list[0]

                target = self.root.findall(
                    ".//rng:define[@name='{0}']".format(ref.attrib.get('name')), self.root.nsmap)[0]
                return target
            else:
                return e.findall('.//', self.root.nsmap)[0]

        def break_point(x):
            """And now I will break point you"""
            def data(x):
                type = x.attrib.get("type", "no")
                return "data:{0}".format(type)

            def value(x):
                return "not editable:{}".format(x.text)

            def attribute(x):
                inner = x.find('.//')
                inner_tag = tag_name(inner)
                if inner_tag == "data":
                    type = inner.attrib.get("type", "no")
                    inner_tag += ":{0}".format(type)
                if inner_tag == "value":
                    inner_text = inner.text
                    inner_tag += ":{0}".format(inner_text)
                return "attribute:{0}".format(inner_tag)

            get_r = {"data": data,
                     "value": value,
                     "attribute": attribute,
                     }
            cleaned_tag = tag_name(x)
            return get_r.get(cleaned_tag, lambda x: False)(x)

        def get_content(x):
            """Not the structure you deserve, but the one you need right now"""

            r = break_point(x)
            if r:
                return (r, self.relax_doc.getpath(x))
            else:
                definition = self.root.findall(".//rng:define[@name='{0}']".format(
                    self.inside_ref_or_type(x).attrib.get('name')),
                    self.root.nsmap
                )
                if definition:
                    cleaned_childs = list(chain(*self.get_childs(definition)))

                    def inside_child(e):
                        if tag_name(e) in ['optional', 'zeroOrMore', 'oneOrMore']:
                            target = get_cardinality_target(e)
                            return target
                        else:
                            return e

                    def make_key(elem):
                        def name_not_in_meta(elem):
                            sub = elem.find("./rng:ref", self.root.nsmap)
                            if sub is not None:
                                return(sub.attrib.get('name', tag_name(elem)))
                            else:
                                return elem.attrib.get('name', tag_name(elem))

                        def name_if_meta_in_tag(elem):
                            return "{}.{}".format(elem.attrib.get('name', tag_name(elem)),
                                                  get_cardinality_target(elem).attrib.get('name', tag_name(elem)))

#                         print(name_not_in_meta(elem) if tag_name(elem) not in ['optional', 'zeroOrMore', 'oneOrMore'] else\
#                             name_if_meta_in_tag(elem))
                        return name_not_in_meta(elem) if tag_name(elem) not in ['optional', 'zeroOrMore', 'oneOrMore'] else\
                            name_if_meta_in_tag(elem)

                    def make_value(elem):
                        return get_content(elem)
                    return {make_key(elem): make_value(elem) for
                            elem in cleaned_childs}
                else:
                    child = x.findall("./", self.root.nsmap)[0]
                    r = break_point(child)
                    if r:
                        return (r, self.relax_doc.getpath(x))
                    else:
                        return (child.attrib.get('name'), self.relax_doc.getpath(x))

        results[self.target] = {x.attrib.get('name', x.getparent().attrib.get(
            'name')): get_content(x) for x in list(chain(*self.get_childs(definitionx)))}
        return results

    # def find_by_tag_name(self, tag_name):
    #     """finds by tag name"""
    #     return [element for element in self.root.findall(".//{0}".format(tag_name))]

    # def contains_a_reference(self, element):
    #     """
    #     Element containing a reference are the components.
    #     Other ones are their definition.
    #     Returns either matching element either None. Might be usefull somedayyyyyyyy"""
    #     return element.find(".//rng:ref", self.root.nsmap)

    # def find_all(self, array, child_name):
    #     """
    #     finds all
    #     """
    #     return [element.findall(child_name, self.root.nsmap) for element in array]

    # def find_by_attr_val(self, tag, name):
    #     """Too specific, change things here man"""
    #     return [element for element in self.root.findall("rng:*[@{0}='{1}']".format(tag, name), self.root.nsmap)]

    # def all_children(self):
    #     """all children"""
    #     return self.root.findall('.//')

    def inside_ref_or_type(self, element):
        """man"""
        if element is not None:
            found = element.findall(".//rng:ref", self.root.nsmap)
            if found is not None and len(found):
                return found[0]
            else:
                return element.find(".//", self.root.nsmap) or element

    def find_ref(self, element_name):
        """ returns element ref"""
        if element_name is not None:
            found = [x.find(".//rng:ref", self.root.nsmap) for x in self.root.findall(
                ".//rng:define[@name='{0}']".format(element_name), self.root.nsmap)]
            return found[0] if len(found) else None

    def find_def(self, element):
        """when you got the ref, get the definition"""
        if element is not None:
            found = self.root.findall(
                ".//rng:define[@name='{0}']".format(element.attrib.get('name')), self.root.nsmap)
            return found[0] if len(found) else None

    def find_target_ref(self):
        """returns the element in which the target is defined"""
        return self.find_ref(self.target)

    def get_form_root(self, root_name='ArchiveTransfer'):
        return self.root.find(".//rng:define[@name='{0}']".format(root_name),
            self.root.nsmap).find(".//rng:ref", self.root.nsmap).attrib['name']

    def find_definitions(self, the_d={}, target=None):
        """"""
        target = target or self.target
        definition = self.root.find(
            ".//rng:define[@name='{0}']".format(target), self.root.nsmap)
        if(definition):
            ref = definition.xpath(
                ".//rng:ref[@name='{0}']".format(definition.attrib['name']), namespaces=self.root.nsmap)
            if len(ref) == 0:
                ref = self.root.xpath(
                    ".//rng:ref[starts-with(@name,'{0}')]".format(target), namespaces=self.root.nsmap)
        else:
            ref = self.root.xpath(
                ".//rng:ref[starts-with(@name,'{0}')]".format(target), namespaces=self.root.nsmap)
        if(ref):
            name = [e.attrib['name'] for e in ref][0]
            definition2 = self.root.find(
                ".//rng:define[@name='{0}']".format(name), self.root.nsmap)
            all = definition2.findall("*", self.root.nsmap)
            bli = []
            for element in all:
                if tag_name(element) == "data":
                    bli.append("value")
                if tag_name(element) == "value":
                    bli.append("value")
                if tag_name(element) == "attribute":
                    bli.append(element.attrib.get('name'))
                if tag_name(element) == "optional":
                    e = element.find(".//rng:ref", self.root.nsmap)
                    bli.append(e.attrib.get('name'))
                if tag_name(element) in ["element", "oneOrMore", "zeroOrMore"]:
                    elems = [e for e in element.iterchildren(
                        '*') if not e.find(".//rng:ref", self.root.nsmap)]
                    element_name = element.attrib.get('name')
                    targets = [".//rng:ref", ".//rng:data",
                               ".//rng:value", ".//rng:element"]
                    for x in targets:
                        for sub in element.findall(x, self.root.nsmap):
                            if (x != ".//rng:element"):
                                bli.append(sub.attrib.get(
                                    'name', element_name))
                            else:
                                # I don't know if this is either too restrictive OR too specific,
                                # but anyway, it's wrong.
                                if sub.find(".//rng:data", self.root.nsmap) is not None:
                                    bli.append(sub.attrib.get(
                                        'name', element_name))

            names = bli
            # ici tu dois améliorer ton if
            if(len(names)):
                if name not in the_d.keys():
                    the_d[name] = names
            for n in [n for n in names if n not in ["data", "value"]]:
                if n not in the_d.keys():
                    self.find_definitions(the_d, target=n)
        return the_d

    def get_childs(self, element):
        if element is not None:
            #childs = [e.findall("./", self.root.nsmap) for e in element]
            # def child_or_name(x):
            #     return x if "ref" in x.tag else x.attrib.get('name')
            return [e.findall("./", self.root.nsmap) for e in element]
