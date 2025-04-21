# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 17:32:05 2022

@author: yijing
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from eam_create import create_eam

class mainwindow():
    def __init__(self):
        window = tk.Tk()
        window.title("EAM势函数生成器")
            
        screenwidth = window.winfo_screenwidth()        # 获得当前分辨率下窗口的最大宽度
        screenheight = window.winfo_screenheight()
        width = 350;        height = 230    # 设置GUI窗口大小
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        window.geometry(size)               # 设置窗口大小
        
        menubar = tk.Menu(window)
        window.config(menu = menubar)
        
        # 创建一个下拉菜单并将其加入到menu bar里面
        operationmenu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label='菜单', menu=operationmenu)
        operationmenu.add_command(label='关于', command=self.showhelp)
        operationmenu.add_command(label='作者', command=self.showauthor)
        operationmenu.add_command(label='中英对照表', command=self.showlist)
        
        self.database = ['Cu', 'Ag', 'Au', 'Ni', 'Pd', 'Pt', 'Al',
                    'Pb', 'Fe', 'Mo', 'Ta', 'W', 'Mg', 'Co',
                    'Ti','Zr', 'Cr', 'V', 'Nb', '  ']        # Zhou的代码中提供的所有元素
        
        # 设置每一个下拉菜单的具体元素为只读,不允许使用者进行修改,然后调整一下位置 
        label1 = tk.Label(window,text='元素一:')
        label1.grid(row = 1, column= 1, padx=20, pady = 20)
        self.elem1 = ttk.Combobox(window,value=self.database,width=3,state='readonly')
        self.elem1.grid(row = 1, column= 2)
        label2 = tk.Label(window,text='元素二:')
        label2.grid(row = 1, column= 3, padx=20, pady = 20)
        self.elem2 = ttk.Combobox(window,value=self.database,width=3,state='readonly')
        self.elem2.grid(row = 1, column= 4)
        
        label3 = tk.Label(window,text='元素三:')
        label3.grid(row = 2, column= 1, padx=20, pady = 20)
        self.elem3 = ttk.Combobox(window,value=self.database,width=3,state='readonly')
        self.elem3.grid(row = 2, column= 2)
        label4 = tk.Label(window,text='元素四:')
        label4.grid(row = 2, column= 3, padx=20, pady = 20)
        self.elem4 = ttk.Combobox(window,value=self.database,width=3,state='readonly')
        self.elem4.grid(row = 2, column= 4)
        
        label5 = tk.Label(window,text='元素五:')
        label5.grid(row = 3, column= 1, padx=20, pady = 20)
        self.elem5 = ttk.Combobox(window,value=self.database,width=3,state='readonly')
        self.elem5.grid(row = 3, column= 2)
        label6 = tk.Label(window,text='元素六:')
        label6.grid(row = 3, column= 3, padx=20, pady = 20)
        self.elem6 = ttk.Combobox(window,value=self.database,width=3,state='readonly')
        self.elem6.grid(row = 3, column= 4)
        
        # 设置一个按钮输出文件
        output = tk.Button(window,text="生成势函数文件",command=self.writefile)
        output.grid(row=5,column=3)
        
        window.mainloop()
        
    def writefile(self):
        
        # 设置一个空列表存放元素的名字
        ele_list = []
        
        # 获取6个元素的名字
        if self.elem1.get() in self.database and self.elem1.get() != '  ':
            ele_list.append(self.elem1.get())
        if self.elem2.get() in self.database and self.elem2.get() != '  ':
            ele_list.append(self.elem2.get())
        if self.elem3.get() in self.database and self.elem3.get() != '  ':
            ele_list.append(self.elem3.get())
        if self.elem4.get() in self.database and self.elem4.get() != '  ':
            ele_list.append(self.elem4.get())
        if self.elem5.get() in self.database and self.elem5.get() != '  ':
            ele_list.append(self.elem5.get())
        if self.elem6.get() in self.database and self.elem6.get() != '  ':
            ele_list.append(self.elem6.get())
            
        # 去掉列表中重复的元素
        ele_list = list(set(ele_list))
        
        # print(ele_list)  # 此处为debug使用
        
        # 输出文件
        if len(ele_list) != 0:
            create_eam(ele_list)
            outfilename = "".join([*ele_list, ".eam.alloy"])
            info = outfilename + " 生成成功! \n请到程序工作目录下查看."
            messagebox.showinfo('通知',info)
        else:
            messagebox.showerror('错误','请选择至少一个元素!')
            
    def showhelp(self):
        helpinfo = '''
        本GUI基于Zhou老师的python程序编写,调用了python自带的Tkinter库和第三方的numpy库,
        由于目前即使是最多元素的势函数,也只有六元,因此本程序只支持最多6种元素的势函数拟合.
        本程序具有较强的容错能力,能对无选择元素,重复元素的情况进行正确处理,能够支持多达18种不同元素之间的组合,但是请确保拟合的势函数适合用于你所模拟的方向.
        参考文献请查看生成的势函数文件中,开头的CITATION部分的文本.
        '''
        messagebox.showinfo('帮助',helpinfo)
        
    def showauthor(self):
        author = 'GUI Author: hyj from CSU \nCONTRIBUTOR: Xiaowang Zhou, Lucas Hale, Germain Clavier'
        messagebox.showinfo('作者',author)
    def showlist(self):
        List = '''
        Cu(铜)   Ag(银)   Au(金)   Ni(镍)   Pd(钯)   Pt(铂) 
        Al(铝)   Pb(铅)   Fe(铁)   Mo(钼)   Ta(钽)   W(钨)
        Mg(镁)   Co(钴)   Ti(钛)   Zr(锆)   Cr(铬)   V(钒)
        Nb(铌)
        '''
        messagebox.showinfo('中英对照表',List)
mainwindow()