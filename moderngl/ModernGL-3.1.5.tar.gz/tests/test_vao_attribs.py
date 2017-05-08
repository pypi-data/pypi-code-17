import unittest

import ModernGL, struct

class TestCase(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.ctx = ModernGL.create_standalone_context()

	@classmethod
	def tearDownClass(cls):
		cls.ctx.release()

	def test_vao_attribs(self):

		vertex_shader = self.ctx.VertexShader('''
			#version 330

			in vec4 in_vert;
			out vec4 out_vert;

			void main() {
				out_vert = in_vert;
			}
		''')

		program = self.ctx.Program(vertex_shader, ['out_vert'])

		vbo = self.ctx.Buffer(struct.pack('12f', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
		res = self.ctx.Buffer(reserve = struct.calcsize('8f'))

		vao = self.ctx.SimpleVertexArray(program, vbo, '4f', ['in_vert'])
		vao.transform(res, ModernGL.POINTS, 2)

		for a, b in zip(struct.unpack('8f', res.read()), (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)):
			self.assertAlmostEqual(a, b)

		vao.attributes['in_vert'].bind(vbo, 4, 0, 0)
		vao.transform(res, ModernGL.POINTS, 2)

		for a, b in zip(struct.unpack('8f', res.read()), (2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0)):
			self.assertAlmostEqual(a, b)

		vao.attributes['in_vert'].bind(vbo, 8, 20, 0)
		vao.transform(res, ModernGL.POINTS, 2)

		for a, b in zip(struct.unpack('8f', res.read()), (3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0, 11.0)):
			self.assertAlmostEqual(a, b)

		vao.attributes['in_vert'].bind(vbo, 12, 0, 1)
		vao.transform(res, ModernGL.POINTS, 2)

		for a, b in zip(struct.unpack('8f', res.read()), (4.0, 5.0, 6.0, 7.0, 4.0, 5.0, 6.0, 7.0)):
			self.assertAlmostEqual(a, b)


if __name__ == '__main__':
	unittest.main()
