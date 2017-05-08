import unittest

import ModernGL

class TestCase(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.ctx = ModernGL.create_standalone_context()

	@classmethod
	def tearDownClass(cls):
		cls.ctx.release()

	def test_transform(self):

		vertex_shader = self.ctx.VertexShader('''
			#version 330

			in vec4 vert;
			out float vert_length;

			void main() {
				vert_length = length(vert);
			}
		''')

		program = self.ctx.Program(vertex_shader, ['vert_length'])

		self.assertEqual(len(program.shaders), 1)

		self.assertTrue(vertex_shader in program.shaders)

		self.assertIsNot(program.vertex_shader, None)
		self.assertIs(program.fragment_shader, None)
		self.assertIs(program.geometry_shader, None)
		self.assertIs(program.tesselation_evaluation_shader, None)
		self.assertIs(program.tesselation_control_shader, None)

		self.assertIs(program.geometry_input, None)
		self.assertIs(program.geometry_output, None)

		self.assertEqual(len(program.uniforms), 0)
		self.assertEqual(len(program.attributes), 1)

		self.assertEqual(len(program.varyings), 1)
		self.assertEqual(len(program.uniform_blocks), 0)

		self.assertTrue('vert' in program.attributes)
		self.assertTrue('vert' not in program.varyings)

		self.assertTrue('vert_length' not in program.attributes)
		self.assertTrue('vert_length' in program.varyings)


if __name__ == '__main__':
	unittest.main()
