import unittest
from .formats import camel_to_dashed, format_text_row


class TestFormats(unittest.TestCase):
    def test_camel_to_dashed_conversions(self):
        self.assertEqual('hello-world', camel_to_dashed('helloWorld'))
        self.assertEqual('h-w', camel_to_dashed('hW'))
        self.assertEqual('h', camel_to_dashed('h'))
        self.assertEqual('h', camel_to_dashed('H'))
        self.assertEqual('hello-world-again', camel_to_dashed('HelloWorld-Again'))
        # tricky one...
        #self.assertEqual('the-bbc-is-great', camel_to_dashed('theBBCisGreat'))

    def test_format_text_row(self):
        # Some simple values
        self.assertEquals('simple string', format_text_row('simple string'))
        self.assertEquals('1234', format_text_row(1234))
        self.assertEqual('red|green|blue|123', format_text_row(['red', 'green', 'blue', 123], sep="|"))

        # Some dicts
        self.assertEqual('red|green|blue', format_text_row({'a': 'red', 'b': 'green', 'c': 'blue'}, sep='|'))
        self.assertEqual('green|123|red', format_text_row({'zebra': 'red', 'apple': 'green', 'banana': 123}, sep='|'))

        # A simple list of scalars
        self.assertEqual('red\tgreen\tblue\t123', format_text_row(['red', 'green', 'blue', 123]))


    def test_format_as_text(self):
        # A list of lists
        #colors = [
        #    ['red', 'green', 'blue'],
        #    ['cyan', 'magenta', 'yellow', 'black']
        #]
        #self.assertEqual("""red\tgreen\tblue\ncyan\tmagenta\tyellow\tblack""", format_text_row(colors))
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
