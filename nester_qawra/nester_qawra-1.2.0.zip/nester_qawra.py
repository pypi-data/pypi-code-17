def print_lol(the_list,level=0):
    '''
    :BIF isinstance()
    :param the_list:
    :return:

v.1.0.0
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
v.1.1.0
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(each_item)
    '''
def print_lol(the_list,indent=False,level=0):
    '''
    :BIF isinstance()
    :param the_list:
    :return:
    '''

    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='')
            print(each_item)
