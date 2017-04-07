import sys

def print_lol(the_list,indent = False, level = 0,fh = sys.stdout):
        """这个函数取一个位置参数，名为the_list，这可以是任何python列表（也可以是包含嵌套列表的列表），所指定的列表中的每个数据项递归的输出到屏幕上，各个数据占一行.
           第二个参数为level，用来在遇到嵌套列表时，插入制表符
           第三个参数indent来控制何时需要插入制表符
	   第四个参数用来标识将把数据数据写入哪个位置"""	
        for each_items in the_list:
                 if isinstance(each_items, list):
                        print_lol(each_items, indent, level + 1, fh)
                 else:
                        if indent:
                                for tab_stop in range(level):
                                        print("\t",end = '',file = fh)
                        print(each_items , file = fh)
