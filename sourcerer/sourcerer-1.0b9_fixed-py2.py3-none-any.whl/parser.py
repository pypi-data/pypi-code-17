from sourcerer import Document, base_syntax, yaml_syntax
from sys import stdout, argv
import yaml
from pdb import set_trace


class DefaultProcessor(object):

    def __init__(self, parser=None, syntax=base_syntax):
        """ Create a default empty Document

        Args:
            parser (function): The function to parse the file ex. yaml.load, json.loads
        """
        self.doc = Document()
        self.syntax = syntax
        self.parser = parser if parser is not None else lambda x: x

    def load(self, file_name=None, doc=None):
        """ Parse a specification file into a deserialized format

        Args:
            file_name (str): The name of the spec file to load as a string
            doc (Document): A pre-built Document
        """
        if doc is not None:
            self.doc = doc
        else:
            if file_name is not None:
                with open(file_name, 'r') as my_file:
                    parsed_data = self.parser(my_file)
                for section, objects in list(parsed_data.items()):
                    self.doc.add_children(self.assemble(section, objects))

    def assemble(self, object_type, parsed_data):
        """ Process all the nodes in a parsed input document """
        code_objects = []
        if object_type in list(self.syntax.keys()):
            for object_id, object_parameters in list(parsed_data.items()):
                code_obj_class = self.syntax[object_type]['type']
                args, children = self.extract_parameters(object_type,
                                                         object_id,
                                                         object_parameters)
                if self.syntax[object_type]['key'] is not None:
                    args.update({self.syntax[object_type]['key']:object_id})
                code_obj = code_obj_class(**args)
                code_obj.add_children(children)
                code_objects.append(code_obj)
        return code_objects

    def extract_parameters(self, obj_type, obj_id, parameters):
        """ Extract data about code object arguments and children

        Args:
            obj_type (str): The type of object to get data from
            obj_id (str): The key that identified this object in its parent dict
            parameters (dict): The dictionary of properties of the code object to be created
        """
        value_map = self.syntax[obj_type].get('value_map')     # Syntax Map value_map for this code object
        child_map = self.syntax[obj_type].get('children', {})  # Syntax Map child_map for this code object
        code_obj_args = {}
        child_code_objs = []
        for param, param_value in list(parameters.items()):
            if param in list(value_map.keys()):
                code_obj_args[value_map[param]] = param_value
            elif param in list(child_map.keys()):
                child = self.assemble(child_map[param], {param: {child_map[param]: param_value}})
                child_code_objs.extend(child)
        return code_obj_args, child_code_objs

    def output(self, output_file_name=''):
        """ Write out the syntax tree """
        syntax_string = ''.join(self.doc)
        if not output_file_name:
            stdout.write(syntax_string)
        else:
            with open(output_file_name, 'w') as output:
                output.write(syntax_string)

class YAMLProcessor(DefaultProcessor):
    """ A processor that builds a Document from a YAML file """

    def __init__(self, syntax=yaml_syntax):
        super(YAMLProcessor, self).__init__(syntax=syntax, parser=yaml.load)


if __name__ == "__main__":
    gen = YAMLProcessor()
    gen.load(argv[1])
    gen.output()
