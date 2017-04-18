"""Print every item of list """
def print_nest_list(items):
    """Judgement of item"""
    for each_item in items:
        if isinstance(each_item, list):
            print_nest_list(each_item)
        else:
            print(each_item)

