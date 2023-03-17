import tkinter as tk
from tkinter import END


class KeyFrame:

    def __init__(self, key):
        self.master = tk.Tk()
        self.master.title("本地密钥")
        self.master.resizable(False, False)
        self.master.iconbitmap("./image/account.ico")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = 400
        h = 120
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))

        self.master.protocol("WM_DELETE_WINDOW", self.login_break)
        self.create_widgets(key)

    def create_widgets(self, key):
        self.label = tk.Label(self.master, text="请保存好如下密钥，供修改密码、找回保存密码使用")
        self.label.pack(pady=5, padx=5)

        self.text = tk.Text(self.master)
        self.text.pack(padx=10, pady=10)
        self.text.insert(END, key)
        self.text.config(state="disabled")

    def login_break(self):
        self.master.destroy()
        self.master.quit()
