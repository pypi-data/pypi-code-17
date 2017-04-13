import sys
#import mainapp
from notmm.utils.wsgilib import HTTPRequest
from test_support import (
    #WSGIControllerTestCase, 
    TestClient, 
    unittest,
    make_app,
    settings,
    ResponseClass
    )

from model import Message

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        

        self.db = Message().db
        self.author = self.db.Author.findone(username="Etienne Robillard")
        self.msg = Message(
            messageid="12300", 
            author=self.author, 
            content="test")

    def tearDown(self):
        self.db.close()

    #def test_populate(self):
    #    model.setup() 
    #    models = model.get_models()
    #    #print models

    def test_save(self):
        if self.msg.db.conn._is_open:
            print "Database connection is open"
            try:
                #import pdb; pdb.set_trace()
                self.msg.save(commit=False)
            except Exception, e:
                print "rollback() called"
                print e
                self.msg.db.backend.rollback()
            print self.msg

