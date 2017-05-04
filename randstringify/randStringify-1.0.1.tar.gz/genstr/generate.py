abc_STRING = 'abcdefghijklmnopqrstuvwxyz '
ABC_STRING = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
import random
def withLength(l) :
	l = int(l)
	ans = ''
	for i in range(l) :
		x = random.randint(0,26)
		choose = random.randint(0,1)
		if choose == 1:
			ans += abc_STRING[x]
		elif choose == 0 :
			ans += ABC_STRING[x]
	return ans

# print withLength(100)

def withWords(w) :
	w = int(w)
	ans = ''
	i = 0 
	while i != w :
	 	x = random.randint(0,26)
		choose = random.randint(0,1)
		if choose == 1:
			f= abc_STRING[x]
		elif choose == 0 :
			f= ABC_STRING[x]
		
		ans += f
		if (f == ' ') :
			i += 1
	return ans


# print withWords(4)