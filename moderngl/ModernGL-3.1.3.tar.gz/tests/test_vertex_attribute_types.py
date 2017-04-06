import unittest

import ModernGL, struct

vtypes = [
	{
		'version': '330',
		'type': 'int',
		'input': [-1],
		'output': [-2],
	},
	{
		'version': '330',
		'type': 'ivec2',
		'input': [-1, -1],
		'output': [-2, -2],
	},
	{
		'version': '330',
		'type': 'ivec3',
		'input': [-1, -1, -1],
		'output': [-2, -2, -2],
	},
	{
		'version': '330',
		'type': 'ivec4',
		'input': [-1, -1, -1, -1],
		'output': [-2, -2, -2, -2],
	},
	{
		'version': '330',
		'type': 'uint',
		'input': [1],
		'output': [2],
	},
	{
		'version': '330',
		'type': 'uvec2',
		'input': [1, 1],
		'output': [2, 2],
	},
	{
		'version': '330',
		'type': 'uvec3',
		'input': [1, 1, 1],
		'output': [2, 2, 2],
	},
	{
		'version': '330',
		'type': 'uvec4',
		'input': [1, 1, 1, 1],
		'output': [2, 2, 2, 2],
	},
	{
		'version': '330',
		'type': 'float',
		'input': [1.0],
		'output': [2.0],
	},
	{
		'version': '330',
		'type': 'vec2',
		'input': [1.0, 1.0],
		'output': [2.0, 2.0],
	},
	{
		'version': '330',
		'type': 'vec3',
		'input': [1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0],
	},
	{
		'version': '330',
		'type': 'vec4',
		'input': [1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '410',
		'type': 'double',
		'input': [1.0],
		'output': [2.0],
	},
	{
		'version': '410',
		'type': 'dvec2',
		'input': [1.0, 1.0],
		'output': [2.0, 2.0],
	},
	{
		'version': '410',
		'type': 'dvec3',
		'input': [1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0],
	},
	{
		'version': '410',
		'type': 'dvec4',
		'input': [1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '330',
		'type': 'mat2',
		'input': [1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '330',
		'type': 'mat2x3',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '330',
		'type': 'mat2x4',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '330',
		'type': 'mat3x2',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '330',
		'type': 'mat3',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '330',
		'type': 'mat3x4',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '330',
		'type': 'mat4x2',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '330',
		'type': 'mat4x3',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '330',
		'type': 'mat4',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '410',
		'type': 'dmat2',
		'input': [1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '410',
		'type': 'dmat2x3',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '410',
		'type': 'dmat2x4',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '410',
		'type': 'dmat3x2',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '410',
		'type': 'dmat3',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '410',
		'type': 'dmat3x4',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '410',
		'type': 'dmat4x2',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '410',
		'type': 'dmat4x3',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
	{
		'version': '410',
		'type': 'dmat4',
		'input': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
		'output': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
	},
]

class TestCase(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.ctx = ModernGL.create_standalone_context()

	@classmethod
	def tearDownClass(cls):
		cls.ctx.release()

	def test_simple(self):
		vert_src = '''
			#version %(version)s

			in %(type)s v_in;
			out %(type)s v_out;

			void main() {
				v_out = v_in * 2;
			}
		'''

		for vtype in vtypes:
			try:
				prog = self.ctx.Program(self.ctx.VertexShader(vert_src % vtype), ['v_out'])
			except ModernGL.Error:
				# skip when version 410 not supported
				continue

			fmt = ModernGL.detect_format(prog, ['v_in'])
			vbo1 = self.ctx.Buffer(struct.pack(fmt, *vtype['input']))
			vbo2 = self.ctx.Buffer(b'\xAA' * struct.calcsize(fmt))
			vao = self.ctx.SimpleVertexArray(prog, vbo1, fmt, ['v_in'])
			vao.transform(vbo2, ModernGL.POINTS, 1)

			for a, b in zip(struct.unpack(fmt, vbo2.read()), vtype['output']):
				self.assertAlmostEqual(a, b)

	def test_arrays(self):
		vert_src = '''
			#version %(version)s

			in %(type)s v_in[];
			out %(type)s v_out[];

			void main() {
				v_out[0] = v_in[0] * 2;
				v_out[1] = v_in[1] * 2;
			}
		'''

		for vtype in vtypes:
			try:
				prog = self.ctx.Program(self.ctx.VertexShader(vert_src % vtype), ['v_out'])
			except ModernGL.Error:
				# skip when version 410 not supported
				continue

			fmt = ModernGL.detect_format(prog, ['v_in'])
			vbo1 = self.ctx.Buffer(struct.pack(fmt, *(vtype['input'] * 2)))
			vbo2 = self.ctx.Buffer(b'\xAA' * struct.calcsize(fmt))
			vao = self.ctx.SimpleVertexArray(prog, vbo1, fmt, ['v_in'])
			vao.transform(vbo2, ModernGL.POINTS, 1)

			for a, b in zip(struct.unpack(fmt, vbo2.read()), vtype['output'] * 2):
				self.assertAlmostEqual(a, b)


if __name__ == '__main__':
	unittest.main()
