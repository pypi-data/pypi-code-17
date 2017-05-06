from pythonforandroid.toolchain import PythonRecipe

class PipRecipe(PythonRecipe):

    version = '9.0.1'
    url = 'https://github.com/pypa/pip/archive/{version}.tar.gz'
    depends = ['python3crystax']

recipe = PipRecipe()
