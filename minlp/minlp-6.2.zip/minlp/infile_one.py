from minlp.inside_one import infile_two

HELLO_WORLD_MESSAGE = 'Hello world! PyOhio Demo - 3! CLEpy'
def get_message():
    return HELLO_WORLD_MESSAGE

def myfunc():
	print("hello world2")
	print("this is my func")
	print(get_message())

if __name__=="__main__":
	infile_two.kkk()
	print('this is top main loop. on top level.')