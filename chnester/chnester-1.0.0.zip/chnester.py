"""
这是我第一模块
递归输出列表里的所有数据
"""
def print_lol(the_list):
    for item in the_list:
        if isinstance(item,list):
            print_lol(item)
        else:
            print(item)
