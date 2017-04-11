def print_list(list1):
    for char in list1:
        if isinstance(char,list):
            print_list(char)
        else:
            print (char)

        
