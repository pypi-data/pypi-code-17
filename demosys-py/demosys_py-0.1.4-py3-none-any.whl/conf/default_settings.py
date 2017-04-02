"""
Default settings for demosys. Override using a settings module.
"""

# What attributes should be used when generating a settings file
__ORDER__ = ('DEBUG', 'SCREENSHOT_PATH', 'OPENGL', 'WINDOW', 'EFFECTS', 'MUSIC',
             'SHADER_DIRS', 'SHADER_FINDERS', 'TEXTURE_DIRS', 'TEXTURE_FINDERS')

DEBUG = False

SCREENSHOT_PATH = None

# OpenGL context configuration
# version: (MAJOR, MINOR)
# profile: any, core, compat
# forward_compat: Whether we should drop fixed pipeline and only support core
OPENGL = {
    "version": (4, 1),
    "profile": "core",
    "forward_compat": True,
}

# Window size
WINDOW = {
    "size": (1280, 720),
    "fullscreen": False,
    "resizable": False,
    "title": "demosys-py",
    "vsync": True,
    "cursor": False,
}

# Empty effects tuple
EFFECTS = ()

MUSIC = None

# Additional directories shaders can be found
SHADER_DIRS = ()

# Finder
SHADER_FINDERS = (
    'demosys.core.shaderfiles.finders.FileSystemFinder',
    'demosys.core.shaderfiles.finders.EffectDirectoriesFinder'
)

# Additonal directories textures can be found
TEXTURE_DIRS = ()
TEXTURE_FINDERS = (
    'demosys.core.texturefiles.finders.FileSystemFinder',
    'demosys.core.texturefiles.finders.EffectDirectoriesFinder'
)

SHADERS = {
    'vertex_shader_suffix': ('vert', '_vs.glsl', '.glslv'),
    'fragment_shader_suffix': ('frag', '_fs.glsl', '.glslf'),
    'geometry_shader_suffix': ('geom', '_gs.glsl', '.glslg'),
}
