"""
这是我第一模块
递归输出列表里的所有数据
20170406
"""
a = [1,2,3,4,[4.1,4.2,4.3,[4.30,4.31]]]
def print_lol(the_list,indent = False,level = 0):
    for item in the_list:
        if isinstance(item,list):
            print_lol(item,indent,level+1)
        else:
            if indent :
                for tab_stop in range(level):
                    print("\t",end='')
            print(item)
