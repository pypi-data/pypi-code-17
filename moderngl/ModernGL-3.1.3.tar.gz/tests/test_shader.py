import unittest

import ModernGL

class TestCase(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.ctx = ModernGL.create_standalone_context()

	@classmethod
	def tearDownClass(cls):
		cls.ctx.release()

	def test_vertex_shader(self):

		shader = self.ctx.VertexShader('''
			#version 330

			void main() {
				gl_Position = vec4(0, 0, 0, 0);
			}
		''')

	def test_fragment_shader(self):

		shader = self.ctx.FragmentShader('''
			#version 330

			out vec4 color;

			void main() {
				color = vec4(0, 0, 0, 0);
			}
		''')


if __name__ == '__main__':
	unittest.main()
