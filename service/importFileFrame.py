import csv
import tkinter as tk
from tkinter.ttk import *

from dao.accountMapper import Db
from utils.message import importSuccess
from utils.myAES import encode_key, encode_password


class ImportFileFrame:

    def __init__(self, filePath, root):
        self.master = tk.Toplevel(master=root)
        self.master.withdraw()  # 隐藏闪烁
        self.master.update()
        self.master.title("数据导入")
        self.master.resizable(False, False)
        self.master.iconbitmap("./image/account.ico")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = 400
        h = 160
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.deiconify()
        self.path = filePath
        # 将top1设置为模式对话框，top1不关闭无法操作主窗口
        self.master.grab_set()
        # self.master.protocol("WM_DELETE_WINDOW", self.login_break())
        self.create_widgets()

    def create_widgets(self):
        self.label = Label(self.master, text="请在下方输入原始密钥")
        self.label.pack(pady=5, padx=5)

        self.entry = Entry(self.master, width=39)
        self.entry.pack(pady=8)
        self.button = Button(self.master, text="确认", command=self.confirm)
        self.button.pack(pady=5, padx=5)

    def confirm(self):
        db = Db()
        key = self.entry.get()
        with open(self.path, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for i in reader:
                i[3] = encode_password(encode_key(key, i[3]))
                db.insert_account(i[1:])
        importSuccess()
        self.master.quit()
        self.master.destroy()

    def login_break(self):
        self.master.quit()
        self.master.destroy()
