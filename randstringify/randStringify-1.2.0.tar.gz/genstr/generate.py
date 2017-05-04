abc_STRING = 'abcdefghijklmnopqrstuvwxyz '
# ABC_STRING = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
import random
def withLength(l ,**kwargs) :
	s = ''	
	try:
		s = kwargs['custom']
	except :
		s = abc_STRING
	s_abc = ''
	s_ABC = ''
	for a in range(len(s)) :
		# print a
		s_abc += s[a].lower()
		s_ABC += s[a].upper()	
	l = int(l)
	ans = ''
	for i in range(l) :
		x = random.randint(0,len(s)-1)
		choose = random.randint(0,1)
		if choose == 1:
			ans += s_abc[x]
		elif choose == 0 :
			ans += s_ABC[x]
	return ans

# print withLength(100)

def withWords(w , **kwargs) :
	s = ''	
	try:
		s = kwargs['custom']
		if ' ' not in s :
			s += ' '
	except :
		s = abc_STRING
	s_abc = ''
	s_ABC = ''
	for a in range(len(s)) :
		# print a
		s_abc += s[a].lower()
		s_ABC += s[a].upper()		
	w = int(w)
	ans = ' '
	i = 0 
	while i != w :
	 	x = random.randint(0,len(s)-1)
		choose = random.randint(0,1)
		if choose == 1:
			f= s_abc[x]
		elif choose == 0 :
			f= s_ABC[x]	
		if ans[-1] == ' ' and f == ' ' :
			continue
		else :
			ans += f
		if (f == ' ') :
			i += 1
	return ans[1:]

# print '-'*100
# print withWords(4 , custom ='abb8')