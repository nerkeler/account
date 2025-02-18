import sys
import tkinter as tk
import uuid
from tkinter.ttk import *
from tkinter import END

from utils.message import emptyKey, haveKey

display_dict = {
    "720": {
        "width": 460,
        "height": 180
    }, "1080": {
        "width": 500,
        "height": 180
    }, "1440": {
        "width": 600,
        "height": 200
    }, "800": {
        "width": 460,
        "height": 180
    }, "1200": {
        "width": 500,
        "height": 180
    }, "1600": {
        "width": 600,
        "height": 200
    }
}


class KeyFrame:

    def __init__(self, flag):
        self.frame = None
        self.master = tk.Tk()
        self.master.withdraw()  # 隐藏闪烁
        self.master.update()
        self.master.title("本地密钥")
        # self.master.resizable(False, False)
        self.master.iconbitmap("./image/account.ico")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = screen_width / 3.5
        h = screen_height / 5
        if str(screen_height) in display_dict.keys():
            w = display_dict[str(screen_height)]['width']
            h = display_dict[str(screen_height)]['height']
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.deiconify()
        self.master.protocol("WM_DELETE_WINDOW", self.login_break)
        self.create_widgets(flag)

    def create_widgets(self, flag):

        if not flag:
            key = uuid.uuid4().__str__()
            labelTitle = "请保存如下密钥，切勿告知他人"
            buttonTitle = "复制"
        else:
            key = ""
            labelTitle = "请输入原始密钥，切勿告知他人"
            buttonTitle = "粘贴"

        Label(self.master).pack()
        self.label = tk.Label(self.master, text=labelTitle)
        self.label.pack(pady=5, padx=5)

        self.entry = Entry(self.master, width=39)
        self.entry.pack(pady=8)
        self.entry.insert(0, key)
        # self.entry.config(state="disabled")
        self.frame = Frame(self.master)
        self.copyButton = Button(self.frame, text=buttonTitle,
                                 command=lambda: self.copyToBoard() if not flag else self.pasteToBoard())
        self.exit = Button(self.frame, text="确认", command=self.confirm)
        self.frame.pack(padx=10, pady=5)
        self.copyButton.pack(side=tk.LEFT, padx=25)
        self.exit.pack(side=tk.LEFT, padx=25)

    def login_break(self):
        self.master.destroy()
        self.master.quit()
        sys.exit()

    def confirm(self):
        if self.entry.get().strip() == '':
            emptyKey()
            return
        with open('resource/aesKey', 'w', encoding='utf-8') as f:  # 使用with open()新建对象f
            f.write(self.entry.get())
        self.master.destroy()
        self.master.quit()

    def copyToBoard(self):
        self.copyButton.config(text="粘贴")
        self.master.clipboard_clear()
        self.master.clipboard_append(self.entry.get())
        self.label.config(text="复制成功，请妥善保管勿将密钥告知他人!")

    def pasteToBoard(self):
        key = self.master.clipboard_get()
        self.entry.delete(0, END)
        self.entry.insert(0, key)
        self.label.config(text="粘贴成功，请妥善保管勿将密钥告知他人!")
