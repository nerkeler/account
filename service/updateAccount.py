from tkinter import *
import tkinter as tk

from dao.accountMapper import Db
from utils.message import updateSuccess
from tkinter.ttk import *

from utils.myAES import encode_password


class UpdateGui:

    def __init__(self, root):
        self.btn1 = self.btn2 = None
        self.master = Toplevel(master=root)
        self.master.withdraw()  # 隐藏闪烁
        self.master.update()
        self.master.title("账户操作")
        self.master.iconbitmap("./image/account.ico")
        self.account = None
        # 使弹出窗口一直处于主窗口前面
        self.master.transient(root)
        # 将top1设置为模式对话框，top1不关闭无法操作主窗口
        self.master.grab_set()
        self.frame1 = tk.Frame(self.master)
        self.frame2 = tk.Frame(self.master)
        self.frame3 = tk.Frame(self.master)
        self.frame4 = tk.Frame(self.master)
        self.frame5 = tk.Frame(self.master)
        self.frame6 = tk.Frame(self.master)

        v1 = StringVar()
        v2 = StringVar()
        v3 = StringVar()
        v4 = StringVar()
        v5 = StringVar()

        self.entry1 = Entry(self.frame1, textvariable=v1)
        self.entry2 = Entry(self.frame2, textvariable=v2)
        self.entry3 = Entry(self.frame3, textvariable=v3, show="*")
        self.entry4 = Entry(self.frame4, textvariable=v4)
        self.entry5 = Entry(self.frame5, textvariable=v5)

    def tk_init(self, account):
        print("开始创建账户布局")
        self.account = account
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = 269
        h = 280
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.deiconify()
        Label(self.master, text="账户操作").pack(padx=8, pady=8)
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
        self.frame6.pack()
        self.btn1 = Button(self.frame6, text="更新账户", command=self.update_account, state=tk.DISABLED)
        self.btn1.pack(side=LEFT, padx=8, pady=8)
        self.btn2 = Button(self.frame6, text="显示密码", command=self.show)
        self.btn2.pack(side=LEFT, padx=8, pady=8)

        self.create(account)
        self.master.mainloop()

    def update_account(self):
        driver = Db()
        password = self.entry3.get()
        result = encode_password(password)
        data = [self.account[0], self.entry1.get(), self.entry2.get(), result, self.entry4.get(), self.entry5.get()]
        row = driver.update(data)
        print(f"row.rowcount: {row.rowcount}")
        if row.rowcount == 1:
            print("更新数据成功，正在退出查看框")
            updateSuccess()
            self.exit()

    def show(self):
        if self.btn2.cget("text") == "显示密码":
            self.entry3.configure(state="normal")
            self.entry3.configure(show="")
            self.btn2.config(text="隐藏密码")
            self.btn1.config(state=tk.NORMAL)

        else:
            self.entry3.configure(show="*")
            self.entry3.configure(state="readonly")
            self.btn2.config(text="显示密码")
            self.btn1.config(state=tk.DISABLED)

    def exit(self):
        self.master.destroy()
        self.master.quit()

    def create(self, item):
        self.entry1.insert(0, str(item[1]))
        self.entry2.insert(0, str(item[2]))
        self.entry3.insert(0, str(item[3]))
        self.entry3.configure(state="readonly")
        self.entry4.insert(0, str(item[4]))
        self.entry5.insert(0, str(item[5]))
