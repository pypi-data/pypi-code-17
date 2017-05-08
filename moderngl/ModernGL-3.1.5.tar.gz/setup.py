import glob
import os
import platform

from setuptools import Extension, setup

target = platform.system().lower()

if target == 'linux':
	from distutils import sysconfig
	sysconfig._config_vars['OPT'] = sysconfig.get_config_vars()['OPT'].replace('-Wstrict-prototypes', '')

libraries = {
	'windows': ['gdi32', 'opengl32', 'user32'],
	'linux': ['GL', 'dl', 'X11'],
	'darwin': [],
}

extra_compile_args = {
	'windows': [],
	'linux': ['-std=c++11'],
	'darwin': ['-std=c++11'],
}

extra_linker_args = {
	'windows': [],
	'linux': [],
	'darwin': ['-framework', 'OpenGL', '-Wno-deprecated'],
}

ModernGL = Extension(
	name = 'ModernGL.ModernGL',
	include_dirs = ['src'],
	# define_macros = [('MGL_VERBOSE', '1')],
	libraries = libraries[target],
	extra_compile_args = extra_compile_args[target],
	extra_link_args = extra_linker_args[target],
	sources = glob.glob('src/*.cpp'),
)

short_description = 'ModernGL: PyOpenGL alternative'

long_description = '''
'''

keywords = [
	'ModernGL',
	'modern OpenGL',
	'OpenGL',
	'PyOpenGL',
	'visualization',
	'ray-tracing',
	'compute shader',
	'shader',
	'documentation',
	'graphics',
	'GLSL',
	'GPU',
	'GPGPU',
	'nvidia',
	'amd',
	'GL',
	'GLU',
	'GLEXT',
	'WGL',
	'WGLEXT',
	'ARB',
	'GLX',
	'2D',
	'3D',
	'CAD',
	'design',
	'video',
]

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Environment :: MacOS X',
	'Environment :: Win32 (MS Windows)',
	'Environment :: X11 Applications',
	'Intended Audience :: Developers',
	'Intended Audience :: Education',
	'Intended Audience :: Science/Research',
	'License :: OSI Approved :: MIT License',
	'Operating System :: MacOS :: MacOS X',
	'Operating System :: Microsoft :: Windows',
	'Operating System :: OS Independent',
	'Operating System :: Unix',
	'Topic :: Artistic Software',
	'Topic :: Desktop Environment',
	'Topic :: Documentation :: Sphinx',
	'Topic :: Games/Entertainment',
	'Topic :: Multimedia',
	'Topic :: Multimedia :: Graphics',
	'Topic :: Multimedia :: Graphics :: 3D Modeling',
	'Topic :: Multimedia :: Graphics :: 3D Rendering',
	'Topic :: Multimedia :: Video :: Display',
	'Topic :: Scientific/Engineering :: Visualization',
]

args = {
	'name' : 'ModernGL',
	'version' : '3.1.5',
	'description' : short_description,
	'long_description' : long_description.strip(),
	'url' : 'https://github.com/cprogrammer1994/ModernGL',
	'download_url' : 'https://github.com/cprogrammer1994/ModernGL/releases',
	'author' : 'Szabolcs Dombi',
	'author_email' : 'cprogrammer1994@gmail.com',
	'license' : 'MIT',
	'classifiers' : classifiers,
	'keywords' : keywords,
	'packages' : ['ModernGL'],
	'ext_modules' : [ModernGL],
	'platforms' : ['any'],
}

if target == 'windows':
	args['zip_safe'] = False

setup(**args)
