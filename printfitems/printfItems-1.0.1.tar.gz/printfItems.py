def printfItems(container,indent=False,level=0):
                for item in container:
                                if isinstance(item,list):
                                        printfItems(item,indent,level+1)
                                else:
                                        if indent:
                                                for num in range(level):
                                                        print("\t",end='')                                                                      
                                        print(item)
