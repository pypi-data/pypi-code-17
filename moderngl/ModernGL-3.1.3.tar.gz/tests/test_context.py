import unittest

import ModernGL

class TestContext(unittest.TestCase):

	def test_context(self):
		ctx = ModernGL.create_standalone_context()
		ctx.release()


if __name__ == '__main__':
	unittest.main()
