ones = ["", "one ", "two ", "three ", "four ", "five ", "six ", "seven ", "eight ", "nine ", "ten ", "eleven ",
			"twelve ", "thirteen ", "fourteen ", "fifteen ", "sixteen ", "seventeen ", "eighteen ", "nineteen "]

twenties = ["", "", "twenty ", "thirty ", "forty ", "fifty ", "sixty ", "seventy ", "eighty ", "ninety "]


def inr2words(amount):
	rupee = int(amount)
	paise = int((amount-rupee)*100)
	return rupee2words(rupee) + 'Rupees and ' + paise2words(paise) + ' Paise Only'

def rupee2words(rupee):
	return num2word(rupee, "")

def paise2words(paise):
	return num2word(paise, "")

def num2word(num, word):
	if num == 0 and word == "" : return 'zero'
	len_num = len(str(num))
	if len_num == 1 or (len_num == 2 and 10 <= num <= 19):
		word += ones[num]
	elif len_num == 2 and num > 19:
		word += twenties[num/10]+ones[num % 10]
	elif len_num == 3:
		w = ones[num / 100]+"hundred "
		word += num2word(num % 100, w)
	elif (len_num == 4 or len_num == 5) and 1 <= num / 1000 <= 19:
		w = ones[num / 1000] + "thousand "
		word += num2word(num % 1000, w)
	elif len_num == 5:
		w = twenties[num / 10000]
		if (num / 1000) % 10 == 0:
			w += "thousand "
		word += num2word(num % 10000, w)
	elif (len_num == 6 or len_num == 7) and 1 <= num / 100000 <= 19:
		w = ones[num / 100000] + "lakh "
		word += num2word(num % 100000, w)
	elif len_num == 7:
		w = twenties[num / 1000000]
		if (num / 100000) % 10 == 0:
			w += "lakh "
		word += num2word(num % 1000000, w)
	elif len_num >= 8 and 1 <= num / 10000000 <= 19:
		w = ones[num / 10000000] + "crore "
		word += num2word(num % 10000000, w)
	else:
		if num / 10000000 < 10:
			w = twenties[num / 10000000]
			if (num / 1000000) % 10 == 0:
				w += "crore "
			word += num2word(num % 10000000, w)
		else:
			word += num2word(num / 10000000, "")
			word += num2word(num % 10000000, "crore ")
	return word

