'''这是"nester.py"模块，提供了一个名为islist（）的函数，这个函数的作用是打印列表，列表中有可能包含嵌套列表。'''
def islist(a):
#这个函数取一个列表名为a作为参数，所指定的列表中的每一项会（递归的）输出到屏幕上。每个数据用逗号隔开。
   for each in a:
       if isinstance(each,list):
           islist(each)
       else:
           print(each)
