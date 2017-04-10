import unittest

"""
unit test for class names resolution. 
A) test behaviour of F2_Class.__init__(self, class_designator, db_designator=None):
   supposed to handle cases with more than one class with the same name but
   attached to a different database (db_designator  acts as a namespace).

B) test that F2_Connection__getattr__(self, name) handles name spaces
   properly ("my_base:My_Class"  -->  F2_Class('My_Class', Database(name='my_base'))
   
Th. Estier - version 1.2 - june 2005
"""
import F2 

class TestF2_ClassNamesResolution(unittest.TestCase):

    def test_className(self):
        f2 = F2.connect('rpc:localhost:8081')
        tb = getattr(f2, 'TestBase', f2.Database.create(name='TestBase'))
        
        k1 = f2.class_create('K1', schema={'id':f2.String}, database=tb)
        k2 = f2.class_create('K1', schema={'id':f2.String})
        
        k3 = f2.TestBase.K1
        self.assertEqual(k1, k3)
        self.assertNotEqual(k3, k2)
        self.assertEqual(k3.db.name, 'TestBase')
        
        # next expression should raise an exception: because it is ambiguous
        with self.assertRaises(F2.ClassDesignationError) as cm:
            k4 = f2.K1        
        self.assertEqual(cm.exception.message, 'name K1 is ambiguous')
        
if __name__ == '__main__':
    unittest.main()
