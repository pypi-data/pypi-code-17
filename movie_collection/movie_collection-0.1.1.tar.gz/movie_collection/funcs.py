"""
This class object holds your collection of DVDs
It keeps track of the title, length in minutes, and year
released on DVD

getHoursOrMins function allows you to calculate the total amount
of time your movies add up to in either minutes or
hours (decimal form)
Input is either 'minute', 'minutes', 'hour', 'hours'
Not case-sensitive
Minutes are returned in integer, hours are returned in decimal

totalTime function allows you to get the total amount of time in
both hours and minutes
For example, getHourOrMins could return 72 minutes or 1.2 hours
totalTime will return "All movies in my collection add up to 1 hours 
and 12 minutes long"
"""

class Movies(object):
	def __init__(self,storer=None):
		self.collection = []
		self.storer = storer

	def add(self,title,length,year):
		"""
		Add movie to DVD collection
		Here is where title, length in minutes and year
		is added to the current collection
		"""
		self.collection.append(DVD(title,length,year))
		return self

	def title(self,index):
		"Get title of movie"
		return self.collection[index - 1].title

	def length(self,index):
		"Get length of a movie"
		return self.collection[index - 1].length

	def year(self,index):
		"Get year of a movie"
		return self.collection[index - 1].year

	def getHoursOrMins(self,minhour):
		"Total number of minutes for movies"
		if str.lower(str(minhour)) == "minute" or str.lower(str(minhour)) == "minutes":
			sum_time = sum([title.length for title in self.collection])
		elif str.lower(str(minhour)) == "hour" or str.lower(str(minhour)) == "hours":
			sum_time = round(sum([title.length for title in self.collection])/60,2)
		else:
			sum_time = ("Please enter 'minute(s)' or 'hour(s)'")
		return sum_time

	def totalTime(self):
		def floor(n):
			res = int(n)
			return res if res == n or n >= 0 else res-1
		hour = floor(sum([title.length for title in self.collection])/60)
		minute = int((round(sum([title.length for title in self.collection])/60,2) - hour)*60)
		return ("All the movies in my collection add up to {} hours and {} minutes long".format(hour,minute))

	def __len__(self):
		return len(self.collection)

"""
This class creates the entry
for each dvd. Default copy number is 1
"""
class DVD(object):
	def __init__(self,title,length,year):
		self.title = title
		self.length = length
		self.year = year