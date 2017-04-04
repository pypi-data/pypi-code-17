import cloudshell.api.cloudshell_api as cs_api
import cloudshell.helpers.scripts.cloudshell_dev_helpers
from cloudshell.api.common_cloudshell_api import CloudShellAPIError


import json


class CloudshellController:

    def __init__(self, configs):
        
        self.configs = configs
        self.session = ''

        self.session = cs_api.CloudShellAPISession(host=self.configs["quali_server_hostname"],
                                              username=self.configs["quali_admin_username"],
                                              password=self.configs["quali_admin_password"],
                                              domain=self.configs["quali_domain"])


    def create_children(self, device_info):
        parent = self.configs['module_port_map'][str(device_info.brics_model)]

        for module in range(1, parent['modules'] + 1):
            for port in range(1, parent['mod%s' % module] + 1):

                self.session.CreateResource(resourceFamily='General Port', resourceModel='Device Port',
                    resourceName='p1_%s_%s' % (module, port), resourceAddress=port, folderFullPath="",
                    parentResourceFullPath=device_info.brics_name,
                    resourceDescription='')

    def set_resource_attribute(self, resource_full_path, attribute_name, attribute_value):
        try:
            self.session.SetAttributeValue(resourceFullPath=resource_full_path, attributeName=attribute_name, attributeValue=attribute_value)

            print '%s updated %s with value %s' % (resource_full_path, attribute_name, attribute_value)
        except CloudShellAPIError as error:
            print error.message + ' ' + error.code

    def set_resource_attributes(self, attribute_values):
        self.session.SetAttributesValues(resourcesAttributesUpdateRequests=attribute_values)

    def get_attribute_object(self, attribute_name, attribute_value):
        return cs_api.AttributeNameValue(attribute_name, attribute_value)

    def get_resource_by_attribute(self, attribute_name, attribute_value):

        if attribute_name == 'Address':
            return self.session.FindResources(resourceAddress=attribute_value)
        elif attribute_name == 'Name':
            return self.session.FindResources(resourceFullName=attribute_value)

        attribute = cs_api.AttributeNameValue(attribute_name, attribute_value)
        return self.session.FindResources(attributeValues=[attribute])

    def get_attribute_value(self, resource_full_path, attribute_name):
        val='-1'
        try:
            att_list = self.session.GetResourceDetails(resourceFullPath=resource_full_path).ResourceAttributes
            if self.item_in_list(attribute_name, att_list):
                val = self.session.GetAttributeValue(resource_full_path=resource_full_path, attributeName=attribute_name).Value
        except CloudShellAPIError as e:
            print 'CLOUDSHELL API ERROR!!! ' + e.message
        return val

    def item_in_list(self, item, list):
        try:
            index = list.index(item)
            return True
        except:
            return False



