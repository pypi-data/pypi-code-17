import unittest
from .conventions import camel_to_dashed


class TestConventions(unittest.TestCase):
    def test_camel_to_dashed_conversions(self):
        self.assertEqual('hello-world', camel_to_dashed('helloWorld'))
        self.assertEqual('h-w', camel_to_dashed('hW'))
        self.assertEqual('h', camel_to_dashed('h'))
        self.assertEqual('h', camel_to_dashed('H'))
        self.assertEqual('hello-world-again', camel_to_dashed('HelloWorld-Again'))
        # tricky one...
        #self.assertEqual('the-bbc-is-great', camel_to_dashed('theBBCisGreat'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
