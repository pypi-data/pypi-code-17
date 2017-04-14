def printVal(movieList):
	for movie in movieList:
		if isinstance(movie,list):
			printVal(movie)
		else:
			print(movie)
