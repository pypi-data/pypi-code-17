import resteve
import json

from resteve import eve


address = 'spoc-cvl01.spoc.linux'

instance = eve.EveServer(address)
instance.login('admin', 'eve')
print ("*** CONNECTED TO EVE-NG")

users = instance.get_users()
payload = json.loads(users.content)
#print users
print payload
data = payload['data']

dict = {}
for item in data:
    dict[item] = payload['data'][item]['pod']

print dict

