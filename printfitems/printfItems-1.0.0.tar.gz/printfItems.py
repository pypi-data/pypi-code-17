def printfItems(container):
	if isinstance(container,list):
		for item in container:
			if isinstance(item,list):
				printfItems(item)
			else:
				print(item)
	else:
                print(container)
