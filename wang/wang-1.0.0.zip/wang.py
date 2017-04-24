mo=["ss",'\t',['qwq','wqqqqq'],"aa",[2,3,4,5]]
print("\tmo")

    
def ppt(list_1,lv):
    for aa in list_1:
        if isinstance(aa,list):
            ppt(aa,lv)
        else:
            for tab_stop in range(lv):
                print("\t")
            print(aa)
           
