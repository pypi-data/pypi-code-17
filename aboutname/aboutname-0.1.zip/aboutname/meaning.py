def get_mean(name):
	all_words = {
	'a': 'aar paar', 
	'b': 'beautiful', 
	'n': 'natkhat',
	'k': 'kindness', 	
	'i': 'intelligent', 
	't': 'taakatvar',
	's': 'stud',
	}
	meaning_list = []
	print('Your qualities:')
	for letter in name:
		meaning_list.append(all_words[letter])
	for mean in meaning_list:
		print('{0} => {1}'.format(mean[0], mean))
	
	
if __name__ == "__main__":
    import sys
    get_mean(str(sys.argv[1]))

name = str(input("Enter your name: "))
get_mean(name)

