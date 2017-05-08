# pylint: disable=import-error
# pylint: disable=line-too-long
# pylint: disable=wildcard-import
# pylint: disable=mixed-indentation
# pylint: disable=bad-whitespace

class Primitive:
	'''
		https://moderngl.github.io/Primitive.html
	'''

	def __init__(self):
		'''
		'''

TRIANGLES = Primitive()
TRIANGLE_STRIP = Primitive()
TRIANGLE_FAN = Primitive()
LINES = Primitive()
LINE_STRIP = Primitive()
LINE_LOOP = Primitive()
POINTS = Primitive()
LINE_STRIP_ADJACENCY = Primitive()
LINES_ADJACENCY = Primitive()
TRIANGLE_STRIP_ADJACENCY = Primitive()
TRIANGLES_ADJACENCY = Primitive()

BLEND = int
DEPTH_TEST = int
CULL_FACE = int
MULTISAMPLE = int

class Buffer:
	'''
		https://moderngl.github.io/Buffer.html
	'''

	def __init__(self, data = None, reserve = 0, dynamic = False):
		'''
		'''

		self.size = 0

	def read(self, size, offset = 0):
		'''
		'''

	def write(self, data, offset = 0):
		'''
		'''

	def access(self, size, offset = 0, readonly = False):
		'''
		'''

	def release(self):
		'''
		'''

class Program:
	'''
		https://moderngl.github.io/Program.html
	'''

	def __init__(self, shaders, varyings = None):
		'''
		'''

		self.uniforms = {}
		self.uniform_blocks = {}
		self.attributes = {}
		self.varyings = {}

	def release(self):
		'''
		'''

class Shader:
	'''
		https://moderngl.github.io/Shader.html
	'''

class VertexShader:
	'''
		https://moderngl.github.io/Shader.html
	'''

	def __init__(self, source):
		'''
		'''

		self.source = ''

	def release(self):
		'''
		'''

class FragmentShader:
	'''
		https://moderngl.github.io/Shader.html
	'''

	def __init__(self, source):
		'''
		'''

		self.source = ''

	def release(self):
		'''
		'''

class GeometryShader:
	'''
		https://moderngl.github.io/Shader.html
	'''

	def __init__(self, source):
		'''
		'''

		self.source = ''

	def release(self):
		'''
		'''

class TessEvaluationShader:
	'''
		https://moderngl.github.io/Shader.html
	'''

	def __init__(self, source):
		'''
		'''

		self.source = ''

	def release(self):
		'''
		'''

class TessControlShader:
	'''
		https://moderngl.github.io/Shader.html
	'''

	def __init__(self, source):
		'''
		'''

		self.source = ''

	def release(self):
		'''
		'''

class VertexArray:
	'''
		https://moderngl.github.io/VertexArray.html
	'''

	def __init__(self, program, content, index_buffer = None, skip_errors = False):
		'''
		'''

	def render(self, mode = TRIANGLES, vertices = 1, first = 0, instances = 1):
		'''
		'''

	def transform(self, output, mode = POINTS, vertices = 1, first = 0, instances = 1):
		'''
		'''

	def release(self):
		'''
		'''

class SimpleVertexArray:
	'''
		https://moderngl.github.io/VertexArray.html
	'''

	def __init__(self, program, buffer, format, attributes, index_buffer = None, skip_errors = False):
		'''
		'''

	def render(self, mode = TRIANGLES, vertices = 1, first = 0, instances = 1):
		'''
		'''

	def transform(self, output, mode = POINTS, vertices = 1, first = 0, instances = 1):
		'''
		'''

	def release(self):
		'''
		'''

class Framebuffer:
	'''
		https://moderngl.github.io/Framebuffer.html
	'''

	def __init__(self, attachments):
		'''
		'''

	def release(self):
		'''
		'''

class Renderbuffer:
	'''
		https://moderngl.github.io/Renderbuffer.html
	'''

	def __init__(self, size, components = 4, floats = True):
		'''
		'''

	def release(self):
		'''
		'''

class DepthRenderbuffer:
	'''
		https://moderngl.github.io/DepthRenderbuffer.html
	'''

	def __init__(self, size):
		'''
		'''

	def release(self):
		'''
		'''

class Texture:
	'''
		https://moderngl.github.io/Texture.html
	'''

	def __init__(self, size, components, data = None, floats = False):
		'''
		'''

	def use(self, location = 0):
		'''
		'''

	def release(self):
		'''
		'''

class DepthTexture:
	'''
		https://moderngl.github.io/DepthTexture.html
	'''

	def __init__(self, size, data = None):
		'''
		'''

	def release(self):
		'''
		'''

class MultisampleRenderbuffer:
	'''
		https://moderngl.github.io/MultisampleRenderbuffer.html
	'''

class MultisampleTexture:
	'''
		https://moderngl.github.io/MultisampleTexture.html
	'''

class Context:
	'''
		https://moderngl.github.io/Context.html
	'''

	def __init__(self):
		'''
		'''

		self.Buffer = Buffer
		self.Program = Program
		self.Shader = Shader
		self.VertexShader = VertexShader
		self.FragmentShader = FragmentShader
		self.GeometryShader = GeometryShader
		self.TessEvaluationShader = TessEvaluationShader
		self.TessControlShader = TessControlShader
		self.VertexArray = VertexArray
		self.SimpleVertexArray = SimpleVertexArray
		self.Framebuffer = Framebuffer
		self.Renderbuffer = Renderbuffer
		self.Texture = Texture
		self.DepthRenderbuffer = DepthRenderbuffer
		self.DepthTexture = DepthTexture
		self.MultisampleRenderbuffer = MultisampleRenderbuffer
		self.MultisampleTexture = MultisampleTexture

	def clear(self, r = 0, g = 0, b = 0, a = 0):
		'''
		'''

	def enable(self, flag):
		'''
		'''

	def disable(self, flag):
		'''
		'''

	def release(self):
		'''
		'''

	def copy_buffer(self, dst, src, size, read_offset, write_offset):
		'''
			copy_buffer(dst, src, size = -1, read_offset = 0, write_offset = 0)
		'''

def create_context():
	'''
		https://moderngl.github.io/ModernGL.html#ModernGL.create_context
	'''

	return Context()

def create_standalone_context():
	'''
		https://moderngl.github.io/ModernGL.html#ModernGL.create_standalone_context
	'''

	return Context()
