import argparse
import logging
import transaction
from AccessControl.SecurityManagement import newSecurityManager
from plone import api
from zope.component.hooks import setSite

logger = logging.getLogger('castle.cms')

parser = argparse.ArgumentParser(
    description='...')
parser.add_argument('--site-id', dest='site_id', default='Castle')
args, _ = parser.parse_known_args()


user = app.acl_users.getUser('admin')  # noqa
newSecurityManager(None, user.__of__(app.acl_users))  # noqa
site = app[args.site_id]  # noqa
setSite(site)


for item in api.portal.get().contentItems():
	print('Removing ' + item[0])
	api.content.delete(obj=item[1], check_linkintegrity=False)

site.reindexObject()
transaction.commit()
