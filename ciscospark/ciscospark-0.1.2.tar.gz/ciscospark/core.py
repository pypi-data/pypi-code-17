import json
import requests

from . import constants as C

"""
#TODO: Use **kwargs?
#TODO: investigate options for create() querystring params
#TODO: generalize get, delete methods?
"""

class Auth(object):
  """docstring for Auth"""
  def __init__(self, token):
    super(Auth, self).__init__()
    self.token = token
    self.url = C.BASE_URL + C.VERSION
    self.header = headers = {'authorization': self.token,
                             'content-type': 'application/json'}

  def send_request(self, method, end, data=None, params=None, limit=None):
    # https://developer.ciscospark.com/pagination.html
    result = None
    fullUrl = self.url + end
    data = json.dumps(data)
    response = requests.request(method, fullUrl, headers=self.header, data=data, params=params)
    response.raise_for_status()

    if response.text:
      result = response.json()

    paginationLink = response.headers.get('Link')
    if limit and paginationLink:
      while paginationLink:
        url, rel = self.parseLinkHeader(paginationLink)
        if rel == 'next':
          response = requests.request(C.GET, url, headers=self.header)
          response.raise_for_status()
          paginationLink = response.headers.get('Link')
          items = response.json()['items']
          print len(items)
          result['items'].extend(items)

    return result

  @classmethod
  def clean_query_Dict(cls, query_Dict):
    """removes NoneTypes from the dict
    """
    return {k: v for k, v in query_Dict.items() if v}

  @classmethod
  def parseLinkHeader(cls, linkHeader):
    #<https://api.ciscospark.com/v1/memberships/?max=50&roomId=Y2lzY29zcGFyazovL3VzL1JPT00vNzJmYjcwNDAtMGUyMS0xMWU3LTk3NmItNTU4ZDMwZmQ1YzQy&cursor=cm9vbUlkPTcyZmI3MDQwLTBlMjEtMTFlNy05NzZiLTU1OGQzMGZkNWM0MiZsaW1pdD01MCZiZWZvcmUmYWZ0ZXI9MGVjODc3OTItOTU0NC00NTJlLTkzN2EtNDAyY2U1MzUyMjRm>; rel="next"
    parse = linkHeader.split(';')
    url = parse[0][1:-1]
    rel = parse[1].strip().split('rel=')[1][1:-1]
    return url, rel



class People(Auth):
  """docstring for People"""
  def __init__(self, token):
    super(People, self).__init__(token)
    self.end = 'people/'

  def __getitem__(self, personId):
    return self.get(personId)

  def list(self, email=None, displayName=None, maxResults=C.MAX_RESULT_DEFAULT, limit=C.ALL):
    queryParams = {'email': email,
            'displayName': displayName,
            'max': maxResults}
    queryParams = self.clean_query_Dict(queryParams)
    return self.send_request(C.GET, self.end, params=queryParams, limit=limit)['items']

  def get_my_details(self):
    return self.send_request(C.GET, self.end+'me')

  def get(self, personId): #TODO: return person class
    return self.send_request(C.GET, self.end+personId)



class Rooms(Auth):
  """docstring for Rooms"""

  #TODO (erikchan): search for roon by name
  def __init__(self, token):
    super(Rooms, self).__init__(token)
    self.end = 'rooms/'

  def __getitem__(self, roomId):
    return self.get(roomId)

  def list(self, teamId=None, rType=None, maxResults=C.MAX_RESULT_DEFAULT, limit=C.ALL):
    """
    rType can be DIRECT or GROUP
    """
    queryParams = {'teamId': teamId,
            'type': rType,
            'max': maxResults}
    queryParams = self.clean_query_Dict(queryParams)
    ret = self.send_request(C.GET, self.end, data=queryParams, limit=limit)
    return [Room(self.token, roomData) for roomData in ret['items']]

  def create(self, title):
    """
    :param title: UTF-8 string that can contain emoji bytes
    http://apps.timwhitlock.info/emoji/tables/unicode
    """
    return self.send_request(C.POST, self.end, data={'title':title})

  def get(self, roomId):
    return Room(self.token, self.get_data(roomId))

  def get_data(self, roomId): # what's the difference? one return object one returns dict?
    roomDict = self.send_request(C.GET, self.end+roomId)
    return roomDict

  def update(self, roomId, title): 
    return self.send_request(C.PUT, self.end+roomId, data={'title':title})

  def delete(self, roomId):
    return self.send_request(C.DELETE, self.end+roomId)



class Room(Rooms):
  """docstring for Room"""
  def __init__(self, token, roomId_or_dict):
    super(Room, self).__init__(token)
    self._memberships = Memberships(token)
    self._messages = Messages(token)
    self._data = None

    if isinstance(roomId_or_dict, dict):
      self._data = roomId_or_dict
    else: #is ID
      self._data = self.get_data(roomId_or_dict)
    
    self.id = self._data['id'].encode(C.UTF8)
    self.name = self._data['title'].encode(C.UTF8)

  def __repr__(self):
    return '<Room name={}, id={}>'.format(self.name, self.id)

  def __iadd__(self, addend):
    """
    :param addend: dict w/ keys message string or person (id or email)
    """

    #TODO (erikchan): pass file to serve as upload & add markdown suppourt
    message = addend.get('message')
    markdown = addend.get('markdown')
    files = addend.get('files')

    if message or markdown or files:
      self._messages.create(self.id, text=message, markdown=markdown, files=files)
    if addend.get('person'):
      if '@' in addend.get('person'):
        self._memberships.create(self.id, personEmail=addend.get('person'))
      else: # assume personId
        self._memberships.create(self.id, personId=addend.get('person'))

    return self

  def __isub__(self, subtrahend):
    """
    :param subtrahend: dict w/ keys messageId or person (id or email)
    """

    if subtrahend.get('message'):
      self._messages.delete(subtrahend.get('message'))
    if subtrahend.get('person'):
      membership = self._findMembership(subtrahend.get('person'))
      self._memberships.delete(self.id, membership['id'])
    return self

  @property
  def messages(self):
    return self._messages.list(roomId=self.id)

  @property
  def people(self):
    return self._memberships.list(roomId=self.id)

  def _findMembership(self, string):
    membership = None
    for person in self.people:
      #hmmm check/clean `string` str encodings here?
      if string == person['personEmail'] or string == person['personDisplayName']:
        membership = person
        break
    return membership



class Memberships(Auth):
  """docstring for Memberships"""
  def __init__(self, token):
    super(Memberships, self).__init__(token)
    self.end = 'memberships/'

  def __getitem__(self, membershipId):
    return self.get(membershipId)

  def list(self, roomId=None, personId=None, personEmail=None, maxResults=C.MAX_RESULT_DEFAULT, limit=C.ALL): 
    queryParams = {'roomId': roomId,
                   'personId': personId,
                   'personEmail': personEmail,
                   'max': maxResults}
    queryParams = self.clean_query_Dict(queryParams)
    return self.send_request(C.GET, self.end, params=queryParams, limit=limit)['items']

  def create(self, roomId, personId=None, personEmail=None, isMod=False):
    queryParams = {'roomId': roomId,
                   'personId': personId,
                   'personEmail': personEmail,
                   'isModerator': isMod}
    queryParams = self.clean_query_Dict(queryParams)
    return self.send_request(C.POST, self.end, data=queryParams)

  def get(self, membershipId):
    return self.send_request(C.GET, self.end+membershipId)

  def update(self, membershipId, isMod=False):
    return self.send_request(C.PUT, self.end+membershipId, data={'isModerator': isMod})

  def delete(self, membershipId):
    return self.send_request(C.DELETE, self.end+membershipId)




class Messages(Auth):
  """docstring for Messages"""
  def __init__(self, token):
    super(Messages, self).__init__(token)
    self.end = 'messages/'

  def __getitem__(self, messageId):
    return self.get(messageId)

  def list(self, roomId, before=None, beforeMessage=None, maxResults=C.MAX_RESULT_DEFAULT, limit=C.ALL):
    queryParams = {'roomId': roomId,
                   'before': before,
                   'beforeMessage': beforeMessage,
                   'max': maxResults}
    queryParams = self.clean_query_Dict(queryParams)
    return self.send_request(C.GET, self.end, params=queryParams, limit=limit)['items']

  def create(self, roomId, text=None, markdown=None, files=None, toPersonId=None, toPersonEmail=None):
    queryParams = {'roomId': roomId,
                   'text': text,
                   'markdown': markdown,
                   'files': files,
                   'toPersonId': toPersonId,
                   'toPersonEmail': toPersonEmail}
    queryParams = self.clean_query_Dict(queryParams)
    return self.send_request(C.POST, self.end, data=queryParams)

  def get(self, messageId):
    return self.send_request(C.GET, self.end+messageId)

  def delete(self, messageId):
    return self.send_request(C.DELETE, self.end+messageId)



class Teams(Auth):
  """docstring for Teams"""
  def __init__(self, token):
    super(Teams, self).__init__(token)
    self.end = 'teams/'

    def __getitem__(self, teamId):
      return self.get(teamId)

  def list(self, maxResults=C.MAX_RESULT_DEFAULT, limit=C.ALL): 
    queryParams = {'max': maxResults}
    queryParams = self.clean_query_Dict(queryParams)
    return self.send_request(C.GET, self.end, params=queryParams, limit=limit)['items']

  def create(self, name): #can it be an emoji?
    return self.send_request(C.POST, self.end, data={'name':name})

  def get(self, teamId):
    return self.send_request(C.GET, self.end+teamId)

  def update(self, teamId, name=None):
    queryParams = {'name': name}
    queryParams = self.clean_query_Dict(queryParams)
    return self.send_request(C.PUT, self.end+teamId, data=queryParams)

  def delete(self, teamId):
    return self.send_request(C.DELETE, self.end+teamId)

#TODO: team memberships. Inherit from Memberships? Roll into Memberships?

class WebHooks(Auth):
  """docstring for WebHooks"""
  def __init__(self, token):
    super(WebHooks, self).__init__(token)
    self.end = 'webhooks/'

    def __getitem__(self, webHookId):
      return self.get(webHookId)

  def list(self, maxResults=C.MAX_RESULT_DEFAULT, limit=C.ALL): 
    queryParams = {'max': maxResults}
    queryParams = self.clean_query_Dict(queryParams)
    return self.send_request(C.GET, self.end, params=queryParams, limit=limit)['items']

  def create(self, name, targetUrl=None, resource=None, event=None, _filter=None, secret=None):
    #TODO: test which are req'd & compatible w/ one another
    queryParams = {'name': name,
                   'targetUrl': targetUrl,
                   'resource': resource,
                   'event': event,
                   'filter': _filter,
                   'secret': secret}
    queryParams = self.clean_query_Dict(queryParams)
    return self.send_request(C.POST, self.end, data=queryParams)

  def get(self, webHookId):
    return self.send_request(C.GET, self.end+webHookId)

  def update(self, webHookId, name=None, targetUrl=None):
    queryParams = {'name': name,
                   'targetUrl': targetUrl}
    queryParams = self.clean_query_Dict(queryParams)
    return self.send_request(C.PUT, self.end+webHookId, data=queryParams)

  def delete(self, webHookId):
    return self.send_request(C.DELETE, self.end+webHookId)



class Organizations(object):
  """docstring for Organizations"""
  def __init__(self, token):
    super(Organizations, self).__init__(token)
    self.end = 'organizations/'

  def list(self, maxResults=C.MAX_RESULT_DEFAULT, limit=C.ALL): 
    queryParams = {'max': maxResults}
    queryParams = self.clean_query_Dict(queryParams)
    return self.send_request(C.GET, self.end, params=queryParams, limit=limit)['items']

  def get(self, orgId):
    return self.send_request(C.GET, self.end+orgId)



class Licenses(object):
  """docstring for Licenses"""
  def __init__(self, token):
    super(Organizations, self).__init__(token)
    self.end = 'licenses/'

  def list(self, orgId=None, maxResults=C.MAX_RESULT_DEFAULT, limit=C.ALL): 
    queryParams = {'orgId':orgId,
                   'max': maxResults}
    queryParams = self.clean_query_Dict(queryParams)
    return self.send_request(C.GET, self.end, params=queryParams, limit=limit)['items']

  def get(self, orgId):
    return self.send_request(C.GET, self.end+orgId)



class Roles(object):
  """docstring for Roles"""
  def __init__(self, token):
    super(Organizations, self).__init__(token)
    self.end = 'roles/'

  def list(self, orgId=None, maxResults=C.MAX_RESULT_DEFAULT, limit=C.ALL): 
    queryParams = {'max': maxResults}
    queryParams = self.clean_query_Dict(queryParams)
    return self.send_request(C.GET, self.end, params=queryParams, limit=limit)['items']

  def get(self, roleId):
    return self.send_request(C.GET, self.end+roleId)
