from tkinter import *
#kusegorplay
def Get1(event):
    global s
    l = event.widget
    sel = l.curselection()
    if len(sel) == 1:
        s = l.get(sel[0])
        if s[0] == '-':
            l.selection_clear(sel[0])
        else:
            print (s)

def Get2(event):
    global s1
    l1 = event.widget
    sel1 = l1.curselection()
    if len(sel1) == 1:
        s1 = l1.get(sel1[0])
        if s1[0] == '-':
            l1.selection_clear(sel1[0])
        else:
            print (s1)
#kusegorplay
def new_window(root):
    Demo2 = Toplevel()
    Demo2.geometry('+400+400')
    listbox1 = Listbox(Demo2, height=5, width=15, selectmode=EXTENDED)
    list1 = [u"Net1", u"Net2", u"Net3", u"Net4"]
    for i in list1:
        listbox1.insert(END, i)
    listbox1.pack()
    listbox1.bind("<<ListboxSelect>>", Get2)
    button5 = Button(Demo2, text='Закрыть', width=70, height=5, bg='black', fg='red',font='arial 14')
    button5.pack()
    button5.bind("<Button-1>", new_msg)    
    Demo2.transient(root)
    Demo2.grab_set()

def new_windowe2(root):
    Demo1 = Toplevel()
    Demo1.geometry('+400+400')
    listbox2 = Listbox(Demo1, height=5, width=15, selectmode=EXTENDED)
    list2 = [u"Usb1", u"Usb2", u"Usb3", u"Usb4"]
    for i in list2:
        listbox2.insert(END, i)
    listbox2.pack()
    listbox2.bind("<<ListboxSelect>>", Get1)
    button4 = Button(Demo1, text='Закрыть', width=70, height=5, bg='black', fg='red',font='arial 14')
    button4.pack()
    button4.bind("<Button-1>", new_msg1)
    Demo1.transient(root)
    Demo1.grab_set()
#kusegorplay
def new_windowe3(root):
    Demo5 = Toplevel()
    Demo5.geometry('+400+400')
    label1 = Label(Demo5, text='Мы предупредили!')
    label1.pack()
    Demo5.transient(root)
    Demo5.grab_set()
        
def new_msg(Demo2):
    Demo3 = Toplevel()
    Demo3.geometry('+400+400')
    label2 = Label(Demo3, text='Подключено к: ' + s1)
    label2.pack()
    Demo3.transient(Demo2)
    Demo3.grab_set()
        
def new_msg1(Demo1):
    Demo4 = Toplevel()
    Demo4.geometry('+400+400')
    label3 = Label(Demo4, text='Подключено к: ' + s)
    label3.pack()
    Demo4.transient(Demo1)
    Demo4.grab_set()
def new_msg2(root):
    Demo6 = Toplevel()
    Demo6.geometry('+400+400')
    label4 = Label(Demo6, text='Это прикол!:-) Вот как ты настраивал: ' + s1 + ' ' + s)
    label4.pack()
    Demo6.transient(root)
    Demo6.grab_set()
#kusegorplay
def main():    
    root=Tk()
    root.title(u'Мастер настройки наушников Beats WI_FI')
    button1=Button(root,text='Шаг 1: Настройка беспроводного подключения',width=70,height=5,bg='black',fg='red',font='arial 14')
    button1.pack()
    button1.bind("<Button-1>", new_window)
    button2=Button(root,text='Шаг 2: Настройка проводного подключения',width=70,height=5,bg='black',fg='red',font='arial 14')
    button2.pack()
    button2.bind("<Button-1>", new_windowe2)
    button3=Button(root,text='Шаг 3: Внимание! Для работы беспроводного подключения необходимо проводное!',width=70,height=5,bg='black',fg='red',font='arial 14')
    button3.pack()
    button3.bind("<Button-1>", new_windowe3)
    button3=Button(root,text='Подсоединить!',width=70,height=5,bg='black',fg='red',font='arial 14')
    button3.pack()
    button3.bind("<Button-1>", new_msg2)
    root.mainloop()
