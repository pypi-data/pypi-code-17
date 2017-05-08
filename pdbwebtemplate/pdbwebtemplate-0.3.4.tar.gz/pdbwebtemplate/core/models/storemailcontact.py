from google.appengine.ext import ndb

class StoreEmailContact(ndb.Model):
    created = ndb.DateTimeProperty(auto_now=True)
    sender_id = ndb.StringProperty(default=None)
    sender_name = ndb.StringProperty(default=None)
    sender_phone = ndb.StringProperty(default=None)
    sender_email = ndb.StringProperty(default=None)
    subject = ndb.StringProperty(default=None)
    message = ndb.StringProperty(default=None)
    receiver_email = ndb.StringProperty(default=None)