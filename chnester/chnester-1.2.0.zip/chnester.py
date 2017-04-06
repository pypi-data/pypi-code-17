"""
这是我第一模块
递归输出列表里的所有数据
20170406
"""
def print_lol(the_list,level = 0):
    for item in the_list:
        if isinstance(item,list):
            print_lol(item,level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(item)
