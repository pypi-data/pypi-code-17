import os
import xml.etree.ElementTree as ET

import yaml

import java_types as java_types
import types as types
from src.domain.field import Field

BASE_PATH = 'src/main/java/'
SUB_DIR_PATH = ''
REL_PATH = ''
MAVEN_GROUP_ID = ''

ID = Field('id', java_types.INTEGER)

IS_LOMBOK_SUPPORTED = False

RELATIVE_PACKAGES = {
    types.MODEL: 'model',
    types.REPOSITORY: 'repository',
    types.SERVICE: 'service',
    types.CONTROLLER: 'controller',
}


def load():
    load_from_pom()
    load_from_settings_file()


def load_from_pom():
    """
    There are many settings that need to be read from the pom to
     make the program run correctly. This parses the pom in order
     to get such relevant information such as calculating the root
     directory, determining which dependencies are found, and the like.
    """
    global REL_PATH, MAVEN_GROUP_ID, IS_LOMBOK_SUPPORTED

    xml_tree = ET.parse('pom.xml').getroot()
    if xml_tree is None:
        raise IOError('Could not find pom.xml')

    # Everything is prepended with this version,
    # so lets get it so we can use it down the line
    version = xml_tree.tag.replace('project', '')

    MAVEN_GROUP_ID = xml_tree.find(version + 'groupId').text
    REL_PATH = ('%s/%s/' % (BASE_PATH, MAVEN_GROUP_ID.replace('.', '/'))).replace('//', '/')

    dependencies = xml_tree.find(version + 'dependencies')

    # The generation can behave differently based on dependencies in the project
    # The searches being performed her are the following:
    #
    #       Lombok
    #           - We don't have to define getters and setters when generating model
    #
    if len(dependencies) != 0:
        for dependency in dependencies.findall(version + 'dependency'):
            if dependency.find(version + 'artifactId').text == 'lombok':
                IS_LOMBOK_SUPPORTED = True


def load_from_settings_file():
    """
    Searches configuration options defined for the project in the plaster.yml
     file. Anything properties found should overwrite the defaults and those
     found in the pom. 
    """
    global ID, IS_LOMBOK_SUPPORTED, RELATIVE_PACKAGES

    # Check to see if a settings file
    # is provided, if not, exit early
    if not os.path.isfile('plaster.yml'):
        return

    # yaml#load returns none if there are no
    # settings in the file, so check for that
    yaml_file = yaml.load(open('plaster.yml'))
    if not yaml_file:
        return

    # Checks for a custom id name and type
    id_args = yaml_file.get('id')
    if id_args:
        name = id_args.get('name', ID.name)
        field_type = id_args.get('type', ID.field_type)

        ID = Field(name, field_type)

    # Checks for custom location(s) for file generation
    # For example:
    #
    # dir:
    #   model: custom/location
    #
    # will force model generation to occur in root/custom/location
    # instead of root/model
    dir_args = yaml_file.get('dir')
    if dir_args:
        for gen_type in types.FILES:
            # This overwrites all the packages, but
            # will default to the original if it is
            # not being set in the gen file
            RELATIVE_PACKAGES[gen_type] = dir_args.get(gen_type, RELATIVE_PACKAGES[gen_type])

    # Checks to see if the user wants to manually enable/disable
    # lombok generation
    lombok_args = yaml_file.get('lombok')
    if lombok_args:
        IS_LOMBOK_SUPPORTED = lombok_args.get('enabled', IS_LOMBOK_SUPPORTED)
        if type(IS_LOMBOK_SUPPORTED) != bool:
            raise ValueError("Error reading property 'lombok.enabled'. Expected of type boolean, got %s" %
                             IS_LOMBOK_SUPPORTED)
