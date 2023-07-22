from tkinter import *
window = Tk( )
window.title('grid')
lab1 = Label(window,text='one',  bg='lightyellow',width=15)
lab2 = Label(window,text='two',  bg='lightgreen', width=15)
lab3 = Label(window,text='three',bg='lightblue', width=15)
lab4 = Label(window,text='four', bg='lightgray',width=15)
lab5 = Label(window,text='five', bg='lightpink',width=15)

lab1.grid(row=0,column=0,rowspan=2) # 0行0列
lab2.grid(row=0,column=1)           # 0行1列
lab3.grid(row=0,column=2)           # 0行2列
lab4.grid(row=1,column=1)           # 1行0列
lab5.grid(row=1,column=2,columnspan=2)           # 1行2列

window.mainloop( )
