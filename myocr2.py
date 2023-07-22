# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

import hashlib
import time

LOG_LINE_NUM = 0

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("发票识别工具_v1.0")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1024x768+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
       
        #self.result_data_label = Label(self.init_window_name, text="输出结果")
        #self.result_data_label.grid(row=0, column=12)
        
        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=12, column=12)
        
        
        #文件列表
        self.file_listbox = Listbox(self.init_window_name, selectmode="extended",width=40, height=29)
        self.file_listbox.grid(row=1, column=1, rowspan=10, columnspan=10)
        
        #文本框
        #self.init_data_Text = Text(self.init_window_name, width=67, height=35)  #原始数据录入框
        #self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        
        """
        self.result_data_Text = Text(self.init_window_name, width=70, height=49)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        """
        
        #按钮
        #选择文件夹按钮
        self.path_btn = Button(self.init_window_name, text="选择路径", command=self.select_path,width=10)
        self.path_btn.grid(row=0, column=1)
        
        #全选按钮
        self.select_all_btn = Button(self.init_window_name, text="全选", command=self.str_trans_to_md5,width=10)
        self.select_all_btn.grid(row=0, column=2)
        
        #全不选按钮
        self.select_cancel_btn = Button(self.init_window_name, text="全不选", command=self.str_trans_to_md5,width=10)
        self.select_cancel_btn.grid(row=0, column=3)
 
        #改名按钮
        self.select_cancel_btn = Button(self.init_window_name, text="开始改名", command=self.str_trans_to_md5,width=10)
        self.select_cancel_btn.grid(row=0, column=12)       
        
    


        self.str_trans_to_md5_button = Button(self.init_window_name, text="字符串转MD5", bg="lightblue", width=10,command=self.str_trans_to_md5)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=0, column=16)

        #图片
        """
        image1=ImageTk.PhotoImage(Image.open("image1.jpeg"))
        image_label = Label(self.init_window_name, image=image1) #packing image into the window
        image_label.grid(row=0, column=16)
        """

    #功能函数
    def select_path(self):
        # 打开文件选择对话框，选择路径
        self.path = filedialog.askdirectory(initialdir=self.init_window_name.path)
        self.update_file_list()
            
    def select_all(self):
        # 打开文件选择对话框，选择路径
        self.path = filedialog.askdirectory(initialdir=self.path)
        self.update_file_list()
        
    def select_cancel(self):
        # 打开文件选择对话框，选择路径
        self.path = filedialog.askdirectory(initialdir=self.path)
        self.update_file_list()
    
    def str_trans_to_md5(self):
        src = self.init_data_Text.get(1.0,END).strip().replace("\n","").encode()
        #print("src =",src)
        if src:
            try:
                myMd5 = hashlib.md5()
                myMd5.update(src)
                myMd5_Digest = myMd5.hexdigest()
                #print(myMd5_Digest)
                #输出到界面
                self.result_data_Text.delete(1.0,END)
                self.result_data_Text.insert(1.0,myMd5_Digest)
                self.write_log_to_Text("INFO:str_trans_to_md5 success")
            except:
                self.result_data_Text.delete(1.0,END)
                self.result_data_Text.insert(1.0,"字符串转MD5失败")
        else:
            self.write_log_to_Text("ERROR:str_trans_to_md5 failed")


    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time


    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    ZMJ_PORTAL.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()