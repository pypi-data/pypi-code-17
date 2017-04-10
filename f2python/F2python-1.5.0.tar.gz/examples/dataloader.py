"""loader of data into an F2 Database
   oct 2014 - Th. Estier
   
   takes a CSV file in input, with arbitrary delimiter, first line is supposed to have
   the "column names". If values or column names or quoted ("like" "this"), then
   the loader automatically strips the quotes. Example (with delimiter = '|' ):

	   firstname|lastname|birthdate|city
       "Jean"|"Dujardin"|1965-12-04|Paris
       "Georges"|"Clooney"|1962-04-18|Atlantic City
       ...
    
    with a source file like this, the loader will create a new TupleClass named like
    your sourcefile (without .txt extension), with one attribute per column, and build
    as many new objects as there are lines after the headers. 
"""
import sys, F2

DatabaseName = 'CGD' # Common Ground of Data 
delimiter = '|'

if len(sys.argv) > 1:
	sourceFileName = sys.argv[1]
else:
	print("Usage: give a file name to process on command line.")
	sys.exit()

def stripSuffix(fileName):
	"strip the .txt suffix from the fileName if any..."
	if fileName[-4:] in ('.txt', '.TXT'):
		return fileName[:-4]
	elif fileName[-5:] in ('.data', '.DATA'):
		return fileName[:-5]
	else:
		return fileName
		
def stripQuotes(word):
	if word[0:1] == '"' and word[-1:] == '"':
		return word[1:-1]
	else:
		return word

def splitDataLine(oneLine):
	"split data from oneLine into a list of strings"
	return [stripQuotes(word) for word in oneLine.split(delimiter)]

# Let's start the load...
f2 = F2.connect('rpc:127.0.0.1:8081')

S = f2.String;
with open(sourceFileName) as src:
	headerList = splitDataLine(src.readline()[:-1]) # don't take the last character: \n
	newClass = f2.class_create(className=stripSuffix(sourceFileName), 
	                           database=DatabaseName,
	                           schema=dict([(a,S) for a in headerList]))
	nbObjects = 0
	for dataLine in src:
		dataList = splitDataLine(dataLine[:-1])     # don't take... etc.
		newClass.create(**dict(zip(headerList, dataList)))
		nbObjects += 1
		if nbObjects % 1000 == 0:
			print(nbObjects)
			f2.commit()

f2.close()

	