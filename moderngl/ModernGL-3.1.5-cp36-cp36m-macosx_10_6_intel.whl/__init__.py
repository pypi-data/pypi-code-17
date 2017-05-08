# pylint: disable=import-error
# pylint: disable=line-too-long
# pylint: disable=wildcard-import
# pylint: disable=mixed-indentation
# pylint: disable=bad-whitespace

'''
	ModernGL
'''

try:
	from ModernGL.pylint_mock import *
except ImportError:
	pass

from ModernGL.ModernGL import *

def detect_format(program, attributes):
	'''
		detect_format(program, attributes)
	'''

	return ''.join('%d%s' % (program.attributes[a].array_length * program.attributes[a].dimension, program.attributes[a].shape) for a in attributes)
