import unittest
import acscli.client
import argparse
import uuid
import os
from . import api_defs


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.client = acscli.client.Client('http://localhost:8080/alfresco')
        self.ticket = None
 
    def get_ticket(self, username='admin', password='admin'):
        if self.ticket is not None:
            return self.ticket
        response = self.client.auth.create_ticket(username, password)
        if response.status_code == 201:
            self.ticket = response.json()['entry']['id']
            return self.ticket
        raise ValueError('Unexpected response from create_ticket: '+response.status_code)

    def test_login_and_get_myself(self):
        ticket = self.get_ticket()
        response = self.client.people.single_entity(ticket, '/people/{personId}', argparse.Namespace(personId='-me-'))
        user = response.json()['entry']
        self.assertEquals('admin', user['id'])
        self.assertEquals('Administrator', user['firstName'])
        self.assertEquals('admin@alfresco.com', user['email'])
        self.assertEquals(True, user['enabled'])

    def test_create_person(self):
        ticket = self.get_ticket()
        user_id = 'user_{unique}'.format(unique=uuid.uuid4())
        args = argparse.Namespace(id=user_id,
                                  password='password',
                                  email='email@example.com',
                                  firstName=user_id.capitalize(),
                                  json_data=None)

        response = self.client.people.create_entity(
            ticket,
            '/people',
            args,
            api_defs.apis['people']['operations']['create-person']['properties'])
        self.assertEqual(201, response.status_code)
        user = response.json()['entry']
        self.assertEquals(user_id, user['id'])
        self.assertEquals('email@example.com', user['email'])
        self.assertEquals(None, user.get('lastName'))

    def test_create_person_with_optional_properties(self):
        ticket = self.get_ticket()
        user_id = 'user_{unique}'.format(unique=uuid.uuid4())
        args = argparse.Namespace(id=user_id,
                                  password='password',
                                  email='email@example.com',
                                  firstName=user_id.capitalize(),
                                  lastName='Bloggs',
                                  description='This is a description for '+user_id,
                                  jobTitle='Head Chef',
                                  json_data=None)

        response = self.client.people.create_entity(
            ticket,
            '/people',
            args,
            api_defs.apis['people']['operations']['create-person']['properties'],
            api_defs.apis['people']['operations']['create-person']['optional-properties'])
        self.assertEqual(201, response.status_code)
        user = response.json()['entry']
        self.assertEquals(user_id, user['id'])
        self.assertEquals('email@example.com', user['email'])
        self.assertEquals('Bloggs', user['lastName'])
        self.assertEquals('This is a description for '+user_id, user['description'])
        self.assertEquals('Head Chef', user['jobTitle'])

    def test_create_person_with_json(self):
        ticket = self.get_ticket()
        user_id = 'user_{unique}'.format(unique=uuid.uuid4())
        args = argparse.Namespace(id=user_id,
                                  password='password',
                                  email='email@example.com',
                                  firstName=user_id.capitalize(),
                                  jobTitle='Saviour of the Universe',
                                  json_data='{"lastName": "Smith", "company": {"organization": "MI5"}}')

        response = self.client.people.create_entity(
            ticket,
            '/people',
            args,
            api_defs.apis['people']['operations']['create-person']['properties'],
            api_defs.apis['people']['operations']['create-person']['optional-properties'])
        self.assertEqual(201, response.status_code)
        user = response.json()['entry']
        self.assertEquals(user_id, user['id'])
        self.assertEquals('email@example.com', user['email'])
        self.assertEquals('Smith', user['lastName'])
        self.assertEquals('Saviour of the Universe', user['jobTitle'])
        self.assertEquals('MI5', user['company']['organization'])
        #print('Created user:', user)

    def test_delete_site(self):
        ticket = self.get_ticket()
        site_id = 'site-{unique}'.format(unique=str(uuid.uuid4())[0:8])
        args = argparse.Namespace(id=site_id,
                                  title='Site Titles Rule',
                                  description='This is a site description for '+site_id.capitalize(),
                                  visibility='PUBLIC',
                                  json_data=None)

        # Create a site
        create_site_def = api_defs.apis['sites']['operations']['create-site']
        get_site_def = api_defs.apis['sites']['operations']['get-site']
        response = self.client.sites.create_entity(
            ticket,
            create_site_def['path'],
            args,
            create_site_def['properties'])
        #print(response.json())
        self.assertEqual(201, response.status_code)

        # Pre-condition of delete-site test is that the site must exist
        response = self.client.sites.single_entity(ticket, get_site_def['path'], argparse.Namespace(siteId=site_id))
        self.assertEqual(200, response.status_code)

        # Delete the site
        del_site_def = api_defs.apis['sites']['operations']['delete-site']
        response = self.client.sites.delete_entity(
            ticket,
            del_site_def['path'],
            argparse.Namespace(siteId=site_id))
        self.assertEqual(204, response.status_code)

        # Check the site's been deleted successfully
        response = self.client.sites.single_entity(ticket, get_site_def['path'], argparse.Namespace(siteId=site_id))
        self.assertEqual(404, response.status_code)

    def test_create_site(self):
        ticket = self.get_ticket()
        site_id = 'site-{unique}'.format(unique=str(uuid.uuid4())[0:8])
        args = argparse.Namespace(id=site_id,
                                  title='Site Titles Rule',
                                  description='This is a site description for '+site_id.capitalize(),
                                  visibility='PUBLIC',
                                  json_data=None)

        response = self.client.sites.create_entity(
            ticket,
            '/sites',
            args,
            api_defs.apis['sites']['operations']['create-site']['properties'])
        print(response.json())
        self.assertEqual(201, response.status_code)
        site = response.json()['entry']
        self.assertEquals(site_id, site['id'])
        self.assertEquals('Site Titles Rule', site['title'])
        self.assertEquals('This is a site description for '+site_id.capitalize(), site['description'])

    def test_update_site(self):
        ticket = self.get_ticket()
        site_id = 'site-{unique}'.format(unique=str(uuid.uuid4())[0:8])
        args = argparse.Namespace(id=site_id,
                                  title='Site Titles Rule',
                                  description='This is a site description for '+site_id.capitalize(),
                                  visibility='PUBLIC',
                                  json_data=None)

        # Create a site
        create_site_def = api_defs.apis['sites']['operations']['create-site']
        response = self.client.sites.create_entity(
            ticket,
            create_site_def['path'],
            args,
            create_site_def['properties'])
        print(response.json())
        self.assertEqual(201, response.status_code)

        # Now update it
        args = argparse.Namespace(siteId=site_id,
                                  title='New Title Here',
                                  description='Changed the description for '+site_id.capitalize(),
                                  visibility='PRIVATE',
                                  json_data=None)
        update_site_def = api_defs.apis['sites']['operations']['update-site']
        response = self.client.sites.update_entity(
            ticket,
            update_site_def['path'],
            args,
            update_site_def['properties'],
            update_site_def['optional-properties'])
        print(response)
        self.assertEqual(200, response.status_code)
        site = response.json()['entry']
        self.assertEquals(site_id, site['id'])
        self.assertEquals('New Title Here', site['title'])
        self.assertEquals('Changed the description for '+site_id.capitalize(), site['description'])
        self.assertEquals('PRIVATE', site['visibility'])

    def test_create_folder(self):
        ticket = self.get_ticket()
        node_name = 'folder-{unique}'.format(unique=str(uuid.uuid4())[0:8])
        # Create a folder named node_name within the "My Files" folder (alias = -my-)
        args = argparse.Namespace(nodeId='-my-',
                                  name=node_name,
                                  nodeType='cm:folder',
                                  json_data='{"properties":{"cm:title":"This is a sub-folder of My Files"}}')
        create_node_def = api_defs.apis['nodes']['operations']['create-node']
        response = self.client.nodes.create_entity(
            ticket,
            create_node_def['path'],
            args,
            create_node_def['properties'],
            create_node_def['optional-properties'])
        print(response.json())
        self.assertEqual(201, response.status_code)
        node = response.json()['entry']
        self.assertEquals(node_name, node['name'])
        self.assertEquals('This is a sub-folder of My Files', node['properties']['cm:title'])

    def test_upload_content(self):
        ticket = self.get_ticket()
        node_name = 'example-{unique}.doc'.format(unique=str(uuid.uuid4())[0:8])
        # Create a file within the "My Files" folder (alias = -my-)
        args = argparse.Namespace(nodeId='-my-',
                                  name=node_name,
                                  nodeType='cm:content',
                                  json_data='{}')
        create_node_def = api_defs.apis['nodes']['operations']['create-node']
        response = self.client.nodes.create_entity(
            ticket,
            create_node_def['path'],
            args,
            create_node_def['properties'],
            create_node_def['optional-properties'])
        print(response.json())
        self.assertEqual(201, response.status_code)
        node = response.json()['entry']
        self.assertEquals(node_name, node['name'])

        upload_def = api_defs.apis['nodes']['operations']['upload-content']

        # look for the test data relative to the script being run, if not,
        # then look in the working directory. This is because of differences depending
        # on where/how you run these tests.
        script_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.dirname(script_dir)
        try:
            example_file = open(os.path.join(parent_dir, 'test_data', 'example_content.doc'), 'rb')
        except FileNotFoundError:
            example_file = open(os.path.join('test_data', 'example_content.doc'), 'rb')

        args = argparse.Namespace(nodeId=node['id'],
                                  content=example_file)
        response = self.client.nodes.upload_content(
            ticket,
            upload_def['path'],
            args,
            upload_def['properties'])
        print(response.json())

if __name__ == '__main__':
    unittest.main(verbosity=2)
