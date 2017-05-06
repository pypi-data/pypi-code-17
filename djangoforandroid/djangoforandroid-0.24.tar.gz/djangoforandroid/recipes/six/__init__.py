from pythonforandroid.toolchain import PythonRecipe

class SixRecipe(PythonRecipe):

    version = '1.10.0'
    url = 'https://github.com/benjaminp/six/archive/{version}.tar.gz'
    depends = ['python3crystax']

recipe = SixRecipe()
