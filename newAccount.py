from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import *

from accountMapper import Db


class AddGui:

    def __init__(self):
        self.master = Tk()
        self.master.title("新增账户")

        self.frame1 = tk.Frame(self.master)
        self.frame2 = tk.Frame(self.master)
        self.frame3 = tk.Frame(self.master)
        self.frame4 = tk.Frame(self.master)
        self.frame5 = tk.Frame(self.master)

        v1 = StringVar()
        v2 = StringVar()
        v3 = StringVar()
        v4 = StringVar()
        v5 = StringVar()

        self.entry1 = Entry(self.frame1, textvariable=v1)
        self.entry2 = Entry(self.frame2, textvariable=v2)
        self.entry3 = Entry(self.frame3, textvariable=v3)
        self.entry4 = Entry(self.frame4, textvariable=v4)
        self.entry5 = Entry(self.frame5, textvariable=v5)

    def tk_init(self):
        print("开始创建新增账户布局")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = 269
        h = 266
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))

        Label(self.master, text="添加账号密码").pack(padx=8, pady=8)
        Label(self.frame1, text="网站: ").pack(side=LEFT, padx=8, pady=8)
        Label(self.frame2, text="账号: ").pack(side=LEFT, padx=8, pady=8)
        Label(self.frame3, text="密码: ").pack(side=LEFT, padx=8, pady=8)
        Label(self.frame5, text="网址: ").pack(side=LEFT, padx=8, pady=8)
        Label(self.frame4, text="备注: ").pack(side=LEFT, padx=8, pady=8)

        self.entry1.pack(side=LEFT, padx=8, pady=8)
        self.entry2.pack(side=LEFT, padx=8, pady=8)
        self.entry3.pack(side=LEFT, padx=8, pady=8)
        self.entry4.pack(side=LEFT, padx=8, pady=8)
        self.entry5.pack(side=LEFT, padx=8, pady=8)

        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.frame5.pack()
        self.frame4.pack()

        Button(self.master, text="确定", command=self.add_account).pack()
        self.master.mainloop()

    def add_account(self):

        driver = Db()
        data = [self.entry1.get(), self.entry2.get(), self.entry3.get(),self.entry5.get(), self.entry4.get()]
        row = driver.insert_account(data)
        print(f"row.rowcount: {row.rowcount}")
        if row.rowcount == 1:
            print("新增数据成功，正在退出新增框")
            messagebox.showinfo(title="提示", message="保存成功！")
            self.exit()

    def exit(self):
        self.master.destroy()
        self.master.quit()