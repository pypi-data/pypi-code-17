import unittest

import ModernGL, struct

class TestBuffer(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.ctx = ModernGL.create_standalone_context()

		cls.vert = cls.ctx.VertexShader('''
			#version 330

			in vec2 in_v1;
			in vec2 in_v2;

			out vec2 out_v;

			void main() {
				out_v = in_v1 + in_v2;
			}
		''')

		cls.prog = cls.ctx.Program(cls.vert, ['out_v'])

	@classmethod
	def tearDownClass(cls):
		cls.ctx.release()

	def test_1(self):
		buf_v1 = self.ctx.Buffer(struct.pack('8f', 1, 2, 3, 4, 5, 6, 7, 8))
		buf_v2 = self.ctx.Buffer(struct.pack('2f', 10, 100))
		res = self.ctx.Buffer(reserve = buf_v1.size)

		vao = self.ctx.VertexArray(self.prog, [
			(buf_v1, '2f', ['in_v1']),
			(buf_v2, '2f/i', ['in_v2']),
		])

		vao.transform(res, ModernGL.POINTS);
		tup = struct.unpack('8f', res.read())
		self.assertAlmostEqual(tup[0], 11.0)
		self.assertAlmostEqual(tup[1], 102.0)
		self.assertAlmostEqual(tup[2], 13.0)
		self.assertAlmostEqual(tup[3], 104.0)
		self.assertAlmostEqual(tup[4], 15.0)
		self.assertAlmostEqual(tup[5], 106.0)
		self.assertAlmostEqual(tup[6], 17.0)
		self.assertAlmostEqual(tup[7], 108.0)


if __name__ == '__main__':
	unittest.main()
