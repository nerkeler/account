import tkinter as tk
from tkinter.ttk import *
import webbrowser


# 创建一个窗口
class About:

    def __init__(self, root):

        self.master = tk.Toplevel(master=root)
        self.master.withdraw()  # 隐藏闪烁
        self.master.update()
        self.master.title("关于")
        self.master.resizable(False, False)
        self.master.iconbitmap("./image/account.ico")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = 800
        h = 420
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.deiconify()
        # 将top1设置为模式对话框，top1不关闭无法操作主窗口
        self.master.grab_set()
        # self.master.protocol("WM_DELETE_WINDOW", self.login_break)


        # 创建一个标签，用于显示标题
        title_label = Label(self.master, text="本地密码管理器", font=("Helvetica", 20))
        title_label.pack(pady=20)

        # 创建一个文本框，用于显示段落内容
        paragraph_text = "本地密码管理器用于管理您的账号信息，避免遗忘，相对其他账号管理器，有以下特点：\n\n" \
                         "1. 完全离线，密码加密存储，安全性高\n" \
                         "2. 界面简单，功能完善，易上手\n" \
                         "3. 功能稳定，持续开发，不定时更新\n\n\n" \
                         "BUG反馈：\n\n" \
                         "\t微信：nerkeler\t\tQQ:2739038007\n\n" \

        paragraph_label = Label(self.master, text=paragraph_text, font=("Helvetica", 12), justify="left")
        paragraph_label.pack(pady=10)
        website_label = Label(self.master, text="Github地址", font=("Helvetica", 12),  cursor="hand2")
        website_label.config(foreground="blue")
        website_label.pack(pady=10)
        website_label.bind("<Button-1>", self.open_website)
        website_label = Label(self.master, text="博客地址", font=("Helvetica", 12),  cursor="hand2")
        website_label.config(foreground="blue")
        website_label.pack(pady=10)
        website_label.bind("<Button-1>", self.open_website1)

    # 创建一个超链接，用于访问网站
    def open_website(self, event):
        webbrowser.open_new("https://github.com/nerkeler/account")
    def open_website1(self, event):
        webbrowser.open_new("https://nerkeler.xyz/")

