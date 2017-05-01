from cx_Freeze import setup, Executable

setup(name='urlprase',
      description='prase stuff',
      executables= [Executable("program.py")])
