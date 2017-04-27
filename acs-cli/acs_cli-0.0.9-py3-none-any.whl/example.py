import acscli.auth
import acscli.sites
import acscli.people

# This shows/plays-with example usage of the REST API client implementation (pyfresco?)
# The ACS-CLI tool will use the same client library and will be the reference app for it.


# APIs are arranged at the top level as: Core, Search, Authentication, Discovery, and Workflow
#
# Concentrate on:
#   auth/login/tickets   Authentication
#   people               Core
#   nodes                Core
#


def format_person(person):
    return '  %s (%s, %s)' % (person['id'], person['firstName'], person.get('email', None))


user='csmith'
password='password'

# Log in as admin
admin_ticket = acscli.auth.create_ticket('admin', 'admin')
# show admin's details
person = acscli.people.person(admin_ticket, '-me-')
print('First output of people.person():', format_person(person))

# Create a new person and log in as them
acscli.people.create_person(admin_ticket, user, password, 'charles@example.com', 'Charles')
# Create ticket vs log in (latter would be automatically plumbed into requests and
# would be kept in a .acs/credentials file at the application level)
ticket = acscli.auth.create_ticket(user, password)
person = acscli.people.person(ticket, '-me-')
print('Second output of people.person():', format_person(person))

# Notice how we're having to provide the ticket in all these cases, but would possibly prefer not to.
# Would ACS-CLI support a credentials provider chain? e.g. env vars -> ~/.acs/credentials -> cli params ?
# This may be ok for tickets, but better not to store u/p unless encrypted (support gnome keyring somehow?)
response = acscli.people.list_people(ticket)
print('People:')
if response.status_code == 200:
    json = response.json()
    for person_blob in json['list']['entries']:
        person = person_blob['entry']
        print(format_person(person))
else:
    print('Unable to get people: %d (%s)' % (response.status_code, response.json()['error']['briefSummary']))


response = acscli.sites.list_sites(ticket)
print('Sites:')
# This is starting to seem like something that can be extracted for listing/paging things...
if response.status_code == 200:
    json = response.json()
    for site_blob in json['list']['entries']:
        site = site_blob['entry']
        print('  %s (%s)' % (site['id'], site.get('description', '-no description-')))
else:
    print('Unable to get sites: %d (%s)' % (response.status_code, response.json()['error']['briefSummary']))

