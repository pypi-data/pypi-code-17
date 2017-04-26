from . import test_base

from yodlee import error


class TestError(test_base.Base):

    def test_error(self):
        with self.assertRaises(error.MissingCredentials):
            raise error.get({'errorCode': 'Y001', 'errorMessage': ''})

        with self.assertRaises(error.Error):
            raise error.get({})
