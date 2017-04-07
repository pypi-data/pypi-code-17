"""
将不同信息转化成相同格式
"""
def sanifize(mystring):
    if '-' in mystring:
        mystr='-'
    elif ':' in mystring:
        mystr=':'
    else:
        return mystring
    (pri,nextp)=mystring.split(mystr)
    return (pri+'.'+nextp)
"""
读取文件中的内容
"""
def file_list(file_name):
    try:
        with open(file_name,'r') as f:
            data=f.readline()
            return (data.strip().split(','))
    except:
        print("IO错误")
"""
将数据读入到一个字典当中
"""
def file_dict(file_name):
    try:
        with open(file_name,'r') as f:
            data=f.readline()
            mylist=data.strip().split(',')
            mydict=dict()
            mydict={'name':mylist.pop(0),'date':mylist.pop(0),
                    'time':sorted(set([sanifize(data) for data in mylist]))[0:3]}
            return (mydict)
    except:
        print("IO错误")
        return(NONE)

sarah=file_dict('sarah2.txt')
print(sarah)
print(sarah['name']+'的跑的最快的三次用时：'+str(sarah['time']))

