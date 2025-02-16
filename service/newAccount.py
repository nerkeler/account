from tkinter import *
import tkinter as tk

from dao.accountMapper import Db
from utils.message import saveSuccess
from tkinter.ttk import *
from utils.myAES import aes_encode, encode_password


class AddGui:

    def __init__(self, root):
        # self.rsa = None
        self.master = Toplevel(master=root)
        self.master.withdraw()  # 隐藏闪烁
        self.master.update()
        self.master.title("新增账户")
        self.master.iconbitmap("./image/account.ico")
        # 使弹出窗口一直处于主窗口前面
        self.master.transient(root)
        # 将top1设置为模式对话框，top1不关闭无法操作主窗口
        self.master.grab_set()
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
        self.entry5.bind("<Return>", self.add_account)

    def tk_init(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = screen_width / 6
        h = screen_height / 4.5
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.deiconify()
        Label(self.master, text="添加账号密码").pack(padx=8, pady=8)
        Label(self.frame1, text="网站: ").pack(side=LEFT, padx=8, pady=8)
        Label(self.frame2, text="账号: ").pack(side=LEFT, padx=8, pady=8)
        Label(self.frame3, text="密码: ").pack(side=LEFT, padx=8, pady=8)
        Label(self.frame4, text="网址: ").pack(side=LEFT, padx=8, pady=8)
        Label(self.frame5, text="备注: ").pack(side=LEFT, padx=8, pady=8)

        self.entry1.pack(side=LEFT, padx=8, pady=8)
        self.entry2.pack(side=LEFT, padx=8, pady=8)
        self.entry3.pack(side=LEFT, padx=8, pady=8)
        self.entry4.pack(side=LEFT, padx=8, pady=8)
        self.entry5.pack(side=LEFT, padx=8, pady=8)

        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.frame4.pack()
        self.frame5.pack()

        Button(self.master, text="确定", command=lambda: self.add_account(event="")).pack()
        self.master.mainloop()

    def add_account(self, event):
        driver = Db()
        password = self.entry3.get()
        result = encode_password(password)
        last_index = driver.get_last_index()
        data = [last_index, self.entry1.get(), self.entry2.get(), result, self.entry4.get(), self.entry5.get()]
        row = driver.insert_account(data)
        if row.rowcount == 1:
            saveSuccess()
            self.exit()

    def exit(self):
        self.master.destroy()
        self.master.quit()
