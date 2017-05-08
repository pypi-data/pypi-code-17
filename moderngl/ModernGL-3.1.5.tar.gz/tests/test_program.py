import unittest

import ModernGL

class TestCase(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.ctx = ModernGL.create_standalone_context()

	@classmethod
	def tearDownClass(cls):
		cls.ctx.release()

	def test_program(self):

		vertex_shader = self.ctx.VertexShader('''
			#version 330

			uniform vec2 pos;
			uniform float scale;

			in vec2 vert;
			out vec2 v_vert;

			void main() {
				gl_Position = vec4(pos + vert * scale, 0.0, 1.0);
				v_vert = vert;
			}
		''')

		fragment_shader = self.ctx.FragmentShader('''
			#version 330

			in vec2 v_vert;
			out vec4 color;

			void main() {
				color = vec4(v_vert, 0.0, 1.0);
			}
		''')

		program = self.ctx.Program([vertex_shader, fragment_shader])

		self.assertEqual(len(program.shaders), 2)

		self.assertTrue(vertex_shader in program.shaders)
		self.assertTrue(fragment_shader in program.shaders)

		self.assertIsNot(program.vertex_shader, None)
		self.assertIsNot(program.fragment_shader, None)
		self.assertIs(program.geometry_shader, None)
		self.assertIs(program.tesselation_evaluation_shader, None)
		self.assertIs(program.tesselation_control_shader, None)

		self.assertIs(program.geometry_input, None)
		self.assertIs(program.geometry_output, None)

		self.assertEqual(len(program.uniforms), 2)
		self.assertEqual(len(program.attributes), 1)

		self.assertEqual(len(program.varyings), 0)
		self.assertEqual(len(program.uniform_blocks), 0)

		self.assertTrue('pos' in program.uniforms)
		self.assertTrue('scale' in program.uniforms)
		self.assertTrue('vert' not in program.uniforms)

		self.assertTrue('vert' in program.attributes)
		self.assertTrue('pos' not in program.attributes)


if __name__ == '__main__':
	unittest.main()
