"""Print every item of list """
def print_nest_list(items,indent=False,level=0):
    """Judgement of item"""
    for each_item in items:
        if isinstance(each_item, list):
            print_nest_list(each_item,indent,level+1)
        else:
            if indent:
                for tap_stop in range(level):
                    print('\t',end='')
            print(each_item)

