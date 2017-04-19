from io import BytesIO
import sys
import unittest


from saemref_client import main


class BasicTest(unittest.TestCase):

    def test_help(self):
        sys.stderr = stream = BytesIO()
        try:
            main()
        except SystemExit:
            pass
        finally:
            sys.stderr = sys.__stderr__

        message = stream.getvalue()
        self.assertTrue(message.startswith('usage: '), message)


if __name__ == '__main__':
    unittest.main()
