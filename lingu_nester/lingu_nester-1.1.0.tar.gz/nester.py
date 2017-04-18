"""Print every item of list """
def print_nest_list(items,level):
    """Judgement of item"""
    for each_item in items:
        if isinstance(each_item, list):
            print_nest_list(each_item,level+1)
        else:
            for tap_stop in range(level):
                print('\t',end='')
            print(each_item)

