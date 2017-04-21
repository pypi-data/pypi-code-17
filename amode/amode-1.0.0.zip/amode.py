amode = ["the holy grail", 2000, "terry jones & terry gilliam", 91, ["graham chapman", ["michael palin", "john cleese", "terry gilliam", "eric idle", "terry hones"]]]

def print_log(the_list):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_log(each_item)
        else:
            print(each_item)

print_log(amode)

"""def print_lol(the_list):
    for eatch_item in the_list:
        if isinstance(eatch_item, list):
            print_lol(eatch_item)
        else:
            print(eatch_item)

print_lol(mode)"""
