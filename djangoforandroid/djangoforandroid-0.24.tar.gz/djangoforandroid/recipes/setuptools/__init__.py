from pythonforandroid.toolchain import PythonRecipe

class SetuptoolsRecipe(PythonRecipe):

    version = 'v35.0.2'
    url = 'https://github.com/pypa/setuptools/archive/{version}.tar.gz'
    depends = ['python3crystax']

recipe = SetuptoolsRecipe()
