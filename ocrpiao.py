import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image
from PIL import  ImageEnhance
import configparser


import os,re,time,subprocess

import pytesseract

"""
票据识别工具1.0

1、图形化界面
2、

"""

class piao(object):
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
        self.exe_directory = os.getcwd()    
        self.config_file = self.exe_directory + "/config.ini"
        #print("read params from:"+ self.config_file)
    

        self.init_window_name.title("票据识别工具1.0")
        self.init_window_name.geometry('1068x681+10+10')
        ico_file = self.exe_directory+'/Icons.ico'
        #if os.path.isfile(ico_file):
        #    self.init_window_name.iconphoto(False,tk.PhotoImage(file=ico_file))
        self.init_window_name.iconbitmap(ico_file)

        # params
        """
        # 发票号码第一位
        self.ticket_head = "0"
        # 发票号码长度
        self.ticketno_len = 10
        # 从标志后面找几行
        self.ticketno_line = 6
        # 图像对比度
        self.img_Contrast = 1.2
        # 标识文字
        self.ticket_flag = "业主使用"
        #是否使用标识，不实用的话就从第一行找
        self.flag_inuse = 1
        """
        
        
        if (os.path.isfile(self.config_file)):	 	
            config = configparser.ConfigParser()
            config.read(self.config_file,encoding="utf-8-sig")
            self.ticket_head = config.get("PIAO", "ticket_head",fallback="0")
            self.ticketno_len = config.get("PIAO", "ticketno_len",fallback="10")
            self.ticketno_line = config.get("PIAO", "ticketno_line",fallback="6")
            
            #ticket_lang = config.get("PIAO", "ticket_lang")
            self.ticket_flag = config.get("PIAO", "ticket_flag",fallback="业主使用")
            self.flag_inuse = config.get("PIAO", "flag_inuse",fallback="1")
            
            self.img_Contrast = config.get("PIAO", "img_Contrast",fallback="1.2")
            #debuglevel = int(config.get("PIAO", "debuglevel"))    

        self.create_widgets()

    def create_widgets(self):
        # 创建路径选择按钮
        # 创建文件列表框
        # 创建滚动条
        #self.scrollbar = tk.Scrollbar(self.file_listbox)
        #self.scrollbar.pack(side="right", fill="none")

        # 关联文件列表框和滚动条
        #self.file_listbox.config(yscrollcommand=self.scrollbar.set)
        #self.scrollbar.config(command=self.file_listbox.yview)

               
        # First row 
        #选择目录按钮
        self.select_button = tk.Button(self.init_window_name, text="选择目录", command=self.select_directory)
        
        #改名字按钮
        self.rename_button = tk.Button(self.init_window_name, text="自动改名", command=self.auto_rename)

        #放大
        self.large_button = tk.Button(self.init_window_name, text="图片放大", command=self.load_image_large)

        #文字识别
        self.ocr_button = tk.Button(self.init_window_name, text="文字识别", command=self.ocr_single)

        #参数设置
        self.conf_button = tk.Button(self.init_window_name, text="参数设置", command=self.setup_config)
  
       
                
        # Second row
        #tree = ttk.Treeview(root)
        #tree.grid(row=1, column=0, rowspan=3, sticky='nsew')
        #目录标签
        self.path_name = tk.Label(self.init_window_name,text='当前目录:')
        self.path_label = tk.Label(self.init_window_name,text="")
    
        #文件标签
        self.file_name = tk.Label(self.init_window_name,text='当前文件:')
        self.file_label = tk.Label(self.init_window_name,text='',bd=3)
    
        # Third row
        #文件列表
        #self.file_list = tk.Listbox(self.init_window_name)
        #self.file_list.bind('<<ListboxSelect>>', self.select_file)
        
        
        
        #滚动条
        self.file_list_frame = tk.Frame(self.init_window_name,bd=5)
        self.file_list_frame.grid(row=3, column=0, columnspan=3,rowspan=12,sticky='nsew')

        self.file_list_scrollbar_y = tk.Scrollbar(self.file_list_frame)
        self.file_list_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_list_scrollbar_y.config(width=20)

        self.file_list_scrollbar_x = tk.Scrollbar(self.file_list_frame, orient=tk.HORIZONTAL)
        self.file_list_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.file_list_scrollbar_x.config(width=20)

        self.file_list = tk.Listbox(self.file_list_frame, yscrollcommand=self.file_list_scrollbar_y.set,xscrollcommand=self.file_list_scrollbar_x.set)
        self.file_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.file_list.bind('<<ListboxSelect>>', self.select_file)

        self.file_list_scrollbar_y.config(command=self.file_list.yview)
        self.file_list_scrollbar_x.config(command=self.file_list.xview)
        

     
        #显示图片
        self.image_label = tk.Label(self.init_window_name,text='this is a pic')
    
        # 日志窗口
        self.log_box = tk.Text(self.init_window_name,bd=3)
    
        #位置布局    #位置布局   #位置布局   #位置布局   #位置布局   #位置布局   #位置布局 #位置布局 
        #################################################################################
        self.select_button.grid(row=0, column=0,columnspan=2)
        self.rename_button.grid(row=0, column=2,columnspan=2)
        self.ocr_button.grid(row=0, column=4,columnspan=2)
        self.large_button.grid(row=0, column=6,columnspan=2)
        self.conf_button.grid(row=0, column=8,columnspan=2)

        self.path_name.grid(row=1, column=0,columnspan=1,padx=(5,0))
        self.path_label.grid(row=1, column=1,columnspan=6,padx=(2,0))
        #padx=(0,800))

        self.file_name.grid(row=2, column=0,columnspan=1,padx=(5,0))
        self.file_label.grid(row=2, column=1,columnspan=7,padx=(2,0))
        #,padx=(0,2800))
        
        self.ticket_no = tk.Label(self.init_window_name,text='票据号码：')
        self.ticket_no.grid(row=2, column=8,columnspan=1,padx=(5,0))
        
        
        self.image_label.grid(row=3, column=3, columnspan=6,rowspan=11,sticky='nsew')

        #间隔
        #self.split_line = tk.Label(self.init_window_name, text="")
        #self.split_line.grid(row=7, column=3,  sticky='nsew')

        self.log_box.grid(row=14, column=3, columnspan=6,rowspan=11)
      
      
        # 初始路径为当前工作目录        
        #self.update_file_list()
        self.directory = os.getcwd()

        self.load_files('')
        self.path_label.configure(text=self.exe_directory)
        
        self.load_image(self.exe_directory+"/picview.jpg")
       
        
    def select_directory(self):
    
        directory = filedialog.askdirectory()
        if  len(directory) ==0 :
            return
        self.directory = directory
        self.load_image(self.exe_directory+"/picview.jpg")
        #tree.delete(*tree.get_children())
        #tree.insert('', 'end', text=directory, open=True)
                
        self.path_label.configure(text=self.directory)
        self.file_label.configure(text="File:")   
        self.file_list_scrollbar_y.set(0,0)
        self.file_list_scrollbar_x.set(1,1)
        
        self.file_list.delete(0, 'end')
        self.load_files('')
        
    
    def load_files(self,sub_dir):
        #遍历加载子目录文件        
        os.chdir(self.directory + sub_dir)
        files = os.listdir(os.getcwd())
        
        for file in files:
            if file.startswith('.') or file.endswith('__'):
                # 忽略隐藏目录
                continue
            if os.path.isdir(file):
                #递归加载
                sub_dir += "/"+file                
                self.load_files(sub_dir)                
            if os.path.isfile(file):
                if file.endswith('.jpg') :
                    self.file_list.insert('end', sub_dir+"/"+file)
    
    def select_file(self,event):
        #在文件里面里面选择文件
        selected_item = self.file_list.curselection()
        if selected_item:
            file_name = self.directory + self.file_list.get(selected_item[0])

            #文件名称跟随改变
            self.file_label.configure(text=file_name)  
            self.ticket_no.configure(text="票据号码：")      
                 
            if file_name.endswith('.jpg') :
                self.load_image(file_name)
    
    def load_image(self,file_name):
        if not(file_name.endswith('.jpg')):
            print(file_name + ":not image file\n") 
            return
        
        image_path = file_name
        image = Image.open(image_path)
        image = image.resize((600, 400), Image.LANCZOS)
        if image.mode == "1": # bitmap image
           image = ImageTk.BitmapImage(image, foreground="white")
        else:              # photo image
           image = ImageTk.PhotoImage(image)    
    
        #self.image_label.config(image=image, bg="#000000",width=image.width(), height=image.height())
        
        self.image_label.config(image=image, bg="#000000",width=600, height=400)
        self.image_label.image = image
        
    def load_image_large(self):
        selected_item = self.file_list.curselection()
        if selected_item:
            file_name = self.directory + self.file_list.get(selected_item[0])
                
            if file_name.endswith('.jpg') :
                image_path = file_name
                image = Image.open(image_path)        
                if image.mode == "1": # bitmap image
                    image = ImageTk.BitmapImage(image, foreground="white")
                else:              # photo image
                    image = ImageTk.PhotoImage(image)                    

                #self.image_label.config(image=image, bg="#000000",width=image.width(), height=image.height())
                self.image_label.config(image=image, bg="#000000",width=700, height=500)
                self.image_label.image = image      
                
                
    #-----------------------------------------------------------------#               
    #   文字识别相关方法                                                 #
    #-----------------------------------------------------------------#


    def ocr_single(self):
        #识别一个文件
        #识别列表框中选择的那个文件
        
        #selected_item = self.file_list.curselection()
        #file_name = self.directory + self.file_list.get(selected_item[0])
        file_name = self.file_label["text"]

        if  len(file_name)>0:
            
            print("1识别一个文件",file_name)   
            self.cv2ocr(file_name)
            """     
            self.log_box.delete(1.0,'end')              
            self.log_box.insert('end', "\nreading ...\n")

            result = self.ocr_image2str(file_name)
            print(result)

            self.log_box.delete(1.0,'end')              
            self.log_box.insert('end', result)
        
            print("2获取发票号码：",end='')        
            text = result.split("\n")

            ticket_no = self.get_ticket_no(text)
            print(ticket_no)
            if len(ticket_no) >0 :
                self.ticket_no.configure(text="票据号码："+ticket_no)       
            """
   
    def auto_rename(self):
        #从文件列表中遍历文件，逐个识别改名
        self.log_box.delete(1.0,'end')   
        
        for i in range(self.file_list.size()):
        

            filename = self.file_list.get(i)

            file_name = self.directory + filename
            
            print("识别文件 %d : %s  "%(i,file_name))      
              
            result = self.ocr_image2str(file_name)
            
            text = result.split("\n")
            
            ticket_no = self.get_ticket_no(text)

            if len(ticket_no) >1 :
                print("票据号码：" + ticket_no)                
                self.log_box.insert('end', filename + "  ::  " + ticket_no + "\n")
                
                #改文件名
                #aa/aa.jpg。--> aa/aa-00286.jpg
                #
                newname= file_name.rsplit("/",1)
                midname = newname[1].split(".")
                                
                new_filename = newname[0]+"/"+midname[0]+"-"+ticket_no+".jpg"
                
                print(file_name + " --> " + new_filename)
                time.sleep(2)
                os.rename(file_name,new_filename)
        

    def ocr_image2str(self,image_filename):
        #ocr 1 file     

        #1 是否已经改名的
        #my_rule = r'\d{'+str(self.ticketno_len)+'}.*'
        #matchObj = re.match(my_rule, image_filename,re.M|re.I)
        #if matchObj:
        #   print(" ... 忽略 " ) 
        #   return
        
        ticket_lang = 'chi_sim'
        
        img_Contrast = float(self.img_Contrast)        
            
        try:
            # Use Tesseract to do OCR on the image
            ##result = pytesseract.image_to_string(Image.open(image_filename),lang='chi_sim')
            
            #print("open " + image_filename)
            img = Image.open(image_filename)

            try:
                
                # 调整亮度 为 0 时生成纯黑图像，为 1 时还是原始图像，该值小于1为亮度减弱，大于1为亮度增强，值越大，图像越亮
                #img_raw = ImageEnhance.Brightness(img).enhance(Brightness)

                #调整对比度 为 0 时生成全灰图像，为 1 时还是原始图像，该值越大，图像颜色对比越明显。
                img_raw = ImageEnhance.Contrast(img).enhance(img_Contrast)

                #调整饱和度 为 0 时生成灰度图像，为 1 时还是原始图像，该值越大，图像颜色越饱和。
                #img_raw = ImageEnhance.Color(img).enhance(img_Color)
                

                try:
                    custom_config = r'-l '+ ticket_lang + ' --psm 6'
                    result = pytesseract.image_to_string(img_raw, config=custom_config)
                
                except:
                    result = " can not image_to_string"    
            except:
                result = " can not change img_Contrast"     
        except:
            result = " can not openfile"     
            
            

        return result
        
        
    def get_ticket_no(self,text):
        #从一堆文字里面找 发票号码  
        """"
        tikect_no = "0"
        start_line =0
              
        """
        debuglevel = 0  
        
        ticket_no = "0"
        start_line =0
        
        #根据关键字判断是否发票
        
        if (self.flag_inuse == "1"):
            start_line = self.is_ticket(text) 
            if (start_line < 0 ):
                #print("未找到发票标识")
                return ticket_no
            if debuglevel: 
                print("发票标识在行号：",start_line)
                 
            
        #从   start_line 这一行开始找，找 ticket_head 开头的  连续  ticketno_len 个数字  
           
        is_match = 0
        ticketno_len =  str(int(self.ticketno_len) -1)
        ticketno_head  =  str(self.ticket_head)
        ticketno_line  =  int(self.ticketno_line)
        
        
        #my_rule = r'(0\d{' + ticketno_len + '})'
        #print("1:",repr(my_rule))
        my_rule = ticketno_head + '\d{' + ticketno_len + '}'
        my_rule = r'.*(' + my_rule + ').*'
        #print("2:",repr(my_rule))
        #my_rule = r'.*(\d{7})$'
        if debuglevel:
            print("start_line:",start_line, "end_line:", ticketno_line, "ticketno_len:", my_rule)

        for aa in range(start_line, ticketno_line+start_line):
            if not(is_match):
                try: 
                    ticketObj = re.match(my_rule,text[aa],re.M|re.I)
                    if debuglevel:
                        print(text[aa],"||" + my_rule )
                    if ticketObj :
                        #print(text[i])                    	
                        ticket_no = ticketObj.group(1)
                        is_match = 1 
                except:
                    ticket_no = "0" 

        return ticket_no
        
        
        
    def is_ticket(self,result):    
        #根据关键字判断是否发票
        #返回值>=0 为真
        ticket_index = -1
 
        for i in range(0, len(result)):

            #matchObj = re.match( r'.*(苏.*准印).*',result[i],re.M|re.I)
            #matchObj = re.match( r'.*(专用收据).*',result[i],re.M|re.I)
            
            #print(result[i],self.ticket_flag) 
            i_index = result[i].find(self.ticket_flag) 
            
            #print(i_index)
            if i_index >= 0:
                ticket_index = i
                break	    
        return ticket_index        
                
    #——————————————————————————————————————————————————————————————————————#
    def cv2ocr(self,file_name):
        newname= file_name.rsplit("/",1)
        pic_name  = newname[1]
        os.chdir(newname[0])
        
        img = cv.imread(pic_name)
        # 复制一个一样大小原图片
        #oldImg = np.ones_like(img)
        #oldImg[:] = img[:]
        # 创建一个窗口
        cv.namedWindow('screenshot_img')
        cv.imshow("screenshot_img", img)

        # 监听这个窗口的鼠标事件
        #cv.setMouseCallback('screenshot_img', draw_rectangle, img)
        # 每10毫秒显示一次图片
        while True:
            cv.imshow("screenshot_img", img)
            # 监听每10毫秒是否按退出键
            if cv.waitKey(10) & 0xFF == 27:
                break
        # 销毁所有窗口
        cv.destroyAllWindows()





    
            
    #——————————————————————————————————————————————————————————————————————#
    # 设置参数
    def setup_config(self):
        # 接收弹窗的数据
        res = self.config_params()
        #print(res)
        if res is None: return
        
        # 更改参数
        self.ticket_head, self.ticketno_len,self.ticketno_line, self.img_Contrast,self.ticket_flag,self.flag_inuse = res 
        print(self.ticket_head, self.ticketno_len,self.ticketno_line, self.img_Contrast,self.ticket_flag,self.flag_inuse)
        # 更新界面
        #self.l1.config(text=self.name)
        #if os.path.exists(self.config_file):
        if (1==1):
            print("save to :"+self.config_file)
            
        
            file1=open(self.config_file,mode='w',encoding='utf-8')
            file1.write('[PIAO]\n')
            file1.write('#票据号第一个数字\nticket_head='+self.ticket_head +'\n')
            file1.write('#票据号长度\nticketno_len='+self.ticketno_len +'\n')
            file1.write('#票据号在关键字后第几行\nticketno_line='+self.ticketno_line +'\n')
            file1.write('#判断票号位置的关键字\nticket_flag='+self.ticket_flag +'\n')
            file1.write('#是否判断关键字\nflag_inuse='+self.flag_inuse +'\n')     
            file1.write('#图片对比度（0.8-1.2)\nimg_Contrast='+self.img_Contrast +'\n')                    
            file1.close()
            
                    
            #字体名称，默认是简体中文：chi_sim
            #ticket_lang=chi_sim


    
    
    # 弹窗设置系统参数
    def config_params(self):
        params= [self.ticket_head, self.ticketno_len,self.ticketno_line, self.img_Contrast,self.ticket_flag,self.flag_inuse]

        inputDialog = MyDialog(params)
        self.init_window_name.wait_window(inputDialog) # 这一句很重要！！！
        
        return inputDialog.params
        

            
            
    def change_pic(self,imgfile,level) :
        img = Image.open(imgfile)
        #level = 1.2
        #图像对比度
        #img_1 = ImageEnhance.Color(img).enhance(level)
        #img_2 = ImageEnhance.Brightness(img).enhance(1.2)
        img_dest = ImageEnhance.Contrast(img).enhance(level)

        return img_dest            
		

    


# 参数设置的弹窗
class MyDialog(tk.Toplevel):
    def __init__(self,parms):
        super().__init__()
        self.title('设置系统参数')
        self.geometry('400x300+600+100')
        """
        self.ticket_head = "0"
        self.ticketno_len = 8
        self.ticketno_line = 6
        self.img_Contrast = 0.8
        self.ticket_flag = ""
        self.flag_inuse = "1"
        """
        self.ticket_head, self.ticketno_len,self.ticketno_line, self.img_Contrast,self.ticket_flag,self.flag_inuse = parms 
        
        # 弹窗界面
        self.setup_UI()
        
        
    def setup_UI(self):
    
        self.ticket_head_label = tk.Label(self,text='票号首字:')
        self.ticketno_len_label = tk.Label(self,text='票号长度:')
        self.ticketno_line_label = tk.Label(self,text='结束行:')
        self.img_Contrast_label = tk.Label(self,text='图片对比度:')
        self.ticket_flag_label = tk.Label(self,text='发票标识:')
        self.flag_inuse_label = tk.Label(self,text='启用标识:')
        
        self.split_label = tk.Label(self,text='  ')
        self.split_label.grid(row=0, column=0,rowspan=6,columnspan=4)

        
        self.ticket_head_label.grid(row=1, column=4,columnspan=3)
        self.ticketno_len_label.grid(row=2, column=4,columnspan=3)
        self.ticketno_line_label.grid(row=3, column=4,columnspan=3)
        self.img_Contrast_label.grid(row=4, column=4,columnspan=3)   
        self.ticket_flag_label.grid(row=5, column=4,columnspan=3)  
        self.flag_inuse_label.grid(row=6, column=4,columnspan=3)  
        
        self.ticket_head_text = tk.Text(self,width=8, height=1)
        self.ticketno_len_text = tk.Text(self,width=8, height=1)
        self.ticketno_line_text = tk.Text(self,width=8, height=1)
        self.img_Contrast_text = tk.Text(self,width=8, height=1)
        self.ticket_flag_text = tk.Text(self,width=8, height=1)
        self.flag_inuse_text = tk.Text(self,width=8, height=1)

        self.ticket_head_text.grid(row=1, column=7)
        self.ticketno_len_text.grid(row=2, column=7)
        self.ticketno_line_text.grid(row=3, column=7)
        self.img_Contrast_text.grid(row=4, column=7) 
        self.ticket_flag_text.grid(row=5, column=7)
        self.flag_inuse_text.grid(row=6, column=7) 
        
        
                  
        self.ticket_head_text.insert(1.0, self.ticket_head)
        self.ticketno_len_text.insert(1.0, self.ticketno_len)
        self.ticketno_line_text.insert(1.0, self.ticketno_line)
        self.img_Contrast_text.insert(1.0, self.img_Contrast) 
        self.ticket_flag_text.insert(1.0, self.ticket_flag)
        self.flag_inuse_text.insert(1.0, self.flag_inuse)         

        self.split_label = tk.Label(self,text='')
        self.split_label.grid(row=7, column=0,columnspan=9)        
        
        
        self.ok_button = tk.Button(self, text="确定", command=self.ok)
        self.cancel_button = tk.Button(self, text="取消", command=self.cancel)
        
        self.ok_button.grid(row=8, column=4,columnspan=3)
        self.cancel_button.grid(row=8, column=7,columnspan=3)                
                

    def ok(self):

        #如果加上 .encode() 返回的类型是 bytes  
        #self.ticket_head = self.ticket_head_text.get(1.0,"end-1c").strip().replace("\n","").encode()
        #print(self.ticket_head)
        #print(type(self.ticket_head))
        
        self.ticket_head = self.ticket_head_text.get(1.0,"end-1c").strip().replace("\n","")
        self.ticketno_len = self.ticketno_len_text.get(1.0,"end-1c").strip().replace("\n","")
        self.ticketno_line = self.ticketno_line_text.get(1.0,"end-1c").strip().replace("\n","")
        self.img_Contrast = self.img_Contrast_text.get(1.0,"end-1c").strip().replace("\n","")
        self.ticket_flag = self.ticket_flag_text.get(1.0,"end-1c").strip().replace("\n","")
        self.flag_inuse = self.flag_inuse_text.get(1.0,"end-1c").strip().replace("\n","")

        self.params = [self.ticket_head, self.ticketno_len,self.ticketno_line, self.img_Contrast,self.ticket_flag,self.flag_inuse] # 设置数据
        self.destroy() # 销毁窗口
        
    def cancel(self):
        self.params = None # 空！
        self.destroy()

        
        
    
if __name__ == "__main__":
    root = tk.Tk()
    app = piao(root)
    #app.init_window_name.mainloop()
    root.mainloop()

