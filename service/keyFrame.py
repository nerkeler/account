import tkinter as tk
from tkinter.ttk import *
from tkinter import END


class KeyFrame:

    def __init__(self, key):
        self.master = tk.Tk()
        self.master.withdraw()  # 隐藏闪烁
        self.master.update()
        self.master.title("本地密钥")
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
        self.master.protocol("WM_DELETE_WINDOW", self.login_break)
        self.create_widgets(key)

    def create_widgets(self, key):
        Label(self.master).pack()
        self.label = tk.Label(self.master, text="请保存如下密钥，切勿告知他人")
        self.label.pack(pady=5, padx=5)

        self.entry = Entry(self.master, width=39)
        self.entry.pack(pady=8)
        self.entry.insert(0, key)
        # self.entry.config(state="disabled")
        self.frame = Frame(self.master)
        self.copyButton = Button(self.frame, text="复制", command=self.copyToBoard)
        self.exit = Button(self.frame, text="退出", command=self.login_break)
        self.frame.pack(padx=10, pady=5)
        self.copyButton.pack(side=tk.LEFT, padx=25)
        self.exit.pack(side=tk.LEFT, padx=25)

    def login_break(self):
        self.master.destroy()
        self.master.quit()

    def copyToBoard(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.entry.get())
        self.entry.delete(0, END)
        self.entry.insert(0, "复制成功，请妥善保管勿将密钥告知他人！")
