"""
    这个函数取一个位置参数，名为‘the_list’，这可以是任何python
列表（也可以是包含祥泰列表的列表）。所指定的列表中的每个数据
项会（递归地）输出到屏幕上，各数据项各占一行。
"""
from sys import stdout
def print_lol(the_list, indent=False, level=0, fh=stdout):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1, fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end = '', file=fh)
            print(each_item, file=fh)


