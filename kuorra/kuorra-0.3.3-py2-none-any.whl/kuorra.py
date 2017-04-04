import shutil, errno
import sys
from subprocess import call
import os
from model_generator import Model_generator as model_generator
from api_generator import Api_generator as api_generator


version = '0.3.3'

def copyanything(src, dst):
	try:
		shutil.copytree(src, dst)
	except OSError as exc:
		if exc.errno == errno.ENOTDIR:
			shutil.copy(src, dst)
		else: raise

def new(args):
	name = args[2]
	print 'Creating new project ....'
	print 'Project: {}'.format(name)
	script_path = os.path.abspath(__file__)
	script_dir = os.path.split(script_path)[0]
	rel_path = "mvc"
	abs_file_path = os.path.join(script_dir, rel_path)
	#call(['ls -l'], shell = True)
	copyanything(abs_file_path, name)
	print 'Project created succesful'

def info():
	print 'kuorra V {}'.format(version)
	print 'Author	: Salvador Hernandez Mendoza'
	print 'Email 	: salvadorhm@gmail.com'
	print 'Twiter 	: @salvadorhm'

def help():
	print 'kuorra V {}'.format(version)
	print 'HELP'
	print 'For new project use: kuorra new <<project_name>>'
	print 'Into the project folder use: kuorra dep '
	print 'Fon kuorra info use: info'
	print 'Into the models folder use: kuorra newmodels db_name db_host db_user db_pw '
	print 'Into the models folder use: kuorra model table_name db_name db_host db_user db_pw '
	print 'Into the models folder use: kuorra newapis db_name db_host db_user db_pw '
	print 'Into the models folder use: kuorra api table_name db_name db_host db_user db_pw '
	

def deploy():
	try:
		call(['clear'], shell = False)
		print '*******************************************************'
		print '*kuorra V {}'.format(version)
		print '*  kuorra WebApp Deploy'
		print '*  For OPEN use Crtl + click in URL'
		print '*  For STOP use Crtl + C  '
		print '*******************************************************'
		print '*************    kuorra Console       *****************'
		print '*******************************************************\n'
		call(['python app.py'], shell = True)
	except (KeyboardInterrupt, SystemExit):
		print 'kuorra shutdown..'

def all_models(args):
	name = args[2]
	db_host = args[3]
	db_name = name
	db_user = args[4]
	db_pw = args[5]

	model = model_generator()

	model.db_host = db_host
	model.db_name = db_name
	model.db_user = db_user
	model.db_pw = db_pw

	'''
	print 'host: '+model_generator.db_host
	print 'db_name: '+model_generator.db_name
	print 'db_user: '+model_generator.db_user
	print 'db_pw: '+model_generator.db_pw
	'''

	model.table_name = name

	model.conectar()
	model.generate()

def one_model(args):
	name = args[2]
	db_table = args[3]
	db_host = args[4]
	db_name = name
	db_user = args[5]
	db_pw = args[6]

	model = model_generator()


	model.db_host = db_host
	model.db_name = db_name
	model.db_user = db_user
	model.db_pw = db_pw
	model.table_name = db_table

	'''
	print 'host: '+model_generator.db_host
	print 'table_name: '+ db_table
	print 'db_name: '+model_generator.db_name
	print 'db_user: '+model_generator.db_user
	print 'db_pw: '+model_generator.db_pw
	'''

	model.conectar()
	model.generate_one(db_table)

def all_apis(args):
	name = args[2]
	db_host = args[3]
	db_name = name
	db_user = args[4]
	db_pw = args[5]

	api = api_generator()

	api.db_host = db_host
	api.db_name = db_name
	api.db_user = db_user
	api.db_pw = db_pw

	'''
	print 'host: '+model_generator.db_host
	print 'db_name: '+model_generator.db_name
	print 'db_user: '+model_generator.db_user
	print 'db_pw: '+model_generator.db_pw
	'''

	api.table_name = name

	api.conectar()
	api.generate()

def one_api(args):
	name = args[2]
	db_table = args[3]
	db_host = args[4]
	db_name = name
	db_user = args[5]
	db_pw = args[6]

	api = api_generator()


	api.db_host = db_host
	api.db_name = db_name
	api.db_user = db_user
	api.db_pw = db_pw
	api.table_name = db_table

	'''
	print 'host: '+api_generator.db_host
	print 'table_name: '+ db_table
	print 'db_name: '+api_generator.db_name
	print 'db_user: '+api_generator.db_user
	print 'db_pw: '+api_generator.db_pw
	'''
	
	api.conectar()
	api.generate_one(db_table)

def main():
	try:
		command = sys.argv[1]
		if command == 'new' or command == '-n':
			new(sys.argv)
		elif command == 'info' or command == '-i':
			info()
		elif command == 'dep' or command == '-d':
			deploy()
		elif command == 'help' or command == '-h':
			help()
		elif command == 'newmodels' or command == '-nm':
			all_models(sys.argv)
		elif command == 'model' or command == '-m':
			one_model(sys.argv)
		elif command == 'newapis' or command == '-na':
			all_apis(sys.argv)
		elif command == 'api' or command == '-a':
			one_api(sys.argv)
		else:
			help()
	except Exception as e:
		print 'ERROR'
		help()
		print e.message

if __name__ == "__main__":
	main()