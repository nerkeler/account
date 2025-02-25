import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import webbrowser
from PIL import Image, ImageTk

display_dict = {
    "720": {
        "width": 820,
        "height": 480
    }, "1080": {
        "width": 1000,
        "height": 580
    }, "1440": {
        "width": 1200,
        "height": 600
    }, "800": {
        "width": 820,
        "height": 480
    }, "1200": {
        "width": 1000,
        "height": 580
    }, "1600": {
        "width": 1200,
        "height": 600
    }
}


class FunctionIntroPag:
    def __init__(self, root):
        self.master = tk.Toplevel(master=root)
        self.master.withdraw()  # 隐藏闪烁
        self.master.update()
        self.master.title("关于")
        # self.master.resizable(False, False)
        self.master.iconbitmap("./image/account.ico")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = screen_width / 2.2
        h = screen_height / 3
        if str(screen_height) in display_dict.keys():
            w = display_dict[str(screen_height)]['width']
            h = display_dict[str(screen_height)]['height']
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.deiconify()
        # 将top1设置为模式对话框，top1不关闭无法操作主窗口
        self.master.grab_set()

        self.create_widgets()

    def create_widgets(self):
        self.frame = Frame(self.master)

        # 创建一个标签，用于显示标题
        title_label = Label(self.master, text="本地密码管理器", font=("微软雅黑", 20))
        title_label.pack(pady=20)

        # 创建一个文本框，用于显示段落内容
        # 创建一个文本框，用于显示段落内容
        paragraph_text = "本地密码管理器用于管理您的账号信息，特点：\n\n" \
                         "1. 完全离线，密码加密存储，安全性高\n" \
                         "2. 界面简单，功能完善，易上手\n" \
                         "3. 功能稳定，持续开发，不定时更新\n\n\n" \
                         "您的支持是我坚持下去的动力\n\n" \
                         "BUG反馈：\n" \
                         "\t微信：nerkeler\t\tQQ:2739038007\t\t\n"
        self.paragraph_label = Label(self.frame, text=paragraph_text, font=("微软雅黑", 12), justify="left")
        self.paragraph_label.pack(pady=10, side=LEFT)

        # 加载并显示一张捐赠图片
        donate_image = Image.open("./image/donate.png")
        donate_image = donate_image.resize((233, 272))
        self.donate_photo = ImageTk.PhotoImage(donate_image)
        self.donate_label = Label(self.frame, image=self.donate_photo)
        self.donate_label.pack(pady=10, side=RIGHT)
        self.frame.pack(pady=10)

        web_frame = Frame(self.master)
        website_label = Label(web_frame, text="Github地址", font=("Helvetica", 12), cursor="hand2")
        website_label.config(foreground="blue")
        website_label.pack(pady=10, side=RIGHT, padx=20)
        website_label.bind("<Button-1>", self.open_website)
        website_label = Label(web_frame, text="博客地址", font=("Helvetica", 12), cursor="hand2")
        website_label.config(foreground="blue")
        website_label.pack(pady=10, side=LEFT, padx=20)
        website_label.bind("<Button-1>", self.open_website1)
        web_frame.pack(pady=10)

    # 创建一个超链接，用于访问网站
    def open_website(self, event):
        webbrowser.open_new("https://github.com/nerkeler/account")

    def open_website1(self, event):
        webbrowser.open_new("https://nerkeler.netlify.app/")
