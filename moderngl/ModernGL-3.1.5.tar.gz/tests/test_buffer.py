import unittest

import ModernGL

class TestBuffer(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.ctx = ModernGL.create_standalone_context()

	@classmethod
	def tearDownClass(cls):
		cls.ctx.release()

	def test_buffer_create(self):
		buf = self.ctx.Buffer(data = b'\xAA\x55' * 10)
		self.assertEqual(buf.read(), b'\xAA\x55' * 10)

	def test_buffer_read_write(self):
		buf = self.ctx.Buffer(reserve = 10)
		buf.write(b'abcd')
		self.assertEqual(buf.read(4), b'abcd')
		buf.write(b'abcd', offset = 3)
		self.assertEqual(buf.read(4, offset = 1), b'bcab')
		buf.write(b'abcd', offset = 6)
		self.assertEqual(buf.read(), b'abcabcabcd')
		self.assertEqual(buf.read(offset = 3), b'abcabcd')

	def test_buffer_orphan(self):
		buf = self.ctx.Buffer(reserve = 1024)
		buf.orphan()

	def test_buffer_invalidate(self):
		buf = self.ctx.Buffer(reserve = 1024)
		buf.release()

		self.assertEqual(type(buf), ModernGL.InvalidObject)

		with self.assertRaises(AttributeError):
			buf.read()

	def test_buffer_access(self):
		buf = self.ctx.Buffer(data = b'\xAA\x55' * 10)
		with buf.access() as a:
			self.assertEqual(a.read(), b'\xAA\x55' * 10)

	def test_buffer_reentrant_access(self):
		buf = self.ctx.Buffer(reserve = 1024)
		with buf.access() as a:
			with self.assertRaises(ModernGL.Error):
				buf.read()


if __name__ == '__main__':
	unittest.main()
