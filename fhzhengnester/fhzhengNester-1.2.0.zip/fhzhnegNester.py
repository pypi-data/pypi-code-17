def print_lol(the_list,level=0):
        """这个函数第一个参数是一个列表，它可以是任意形式的列表
            所提供的列表中的各个数据项会（递归地）打印到屏幕上，而且各占一行。
            第二个参数用来在遇嵌套列表时插入制表符，往里缩进一层。"""
        for each_item in the_list:                
                if isinstance(each_item,list):
                        print_lol(each_item,level+1)
                else:
                        for tab_stop in range(level):
                                print('\t',end='')              #每一层缩进，都显示一个TAB制表符
                        print(each_item)
##以下为测试代码
##myList=[
##        '郑丰华',28,'赵吉武汉',300,
##        ['刘乐',21,45000,'一乐乐乐',1],
##        [['李宁','关之之'],123456],
##        123123,123213]

##print(myList)
##print(myList[0])
##print(myList[1])
##print(myList[2])
##print(myList[4][0])

##print_lol(myList)
##print_lol(myList,0)
