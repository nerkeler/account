import ctypes
import logging
import sys
import tkinter as tk
import tkinter.font as tf
from tkinter.ttk import *
from tkinter import END, INSERT

from utils.MyRSA import MyRSA
from utils.logUtil import setup_logging
from utils.message import emptyKey

setup_logging()
logger = logging.getLogger('server')  # 维护一个全局日志对象


class KeyFrame:

    def __init__(self, flag):
        self.frame = None
        self.master = tk.Tk()
        self.master.withdraw()  # 隐藏闪烁
        self.master.update()
        self.master.title("本地密钥")
        # self.master.resizable(False, False)
        self.master.iconbitmap("./image/account.ico")
        self.ft = tf.Font(family='Consolas', size=1)
        self.ft2 = tf.Font(family='微软雅黑', size=2, weight="bold")
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        # 调用api获得当前的缩放因子
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        self.master.tk.call('tk', 'scaling', ScaleFactor / 75)
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = 700
        h = 510
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.myRsa = MyRSA()
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.deiconify()
        self.master.protocol("WM_DELETE_WINDOW", self.login_break)
        self.create_widgets(flag)

    def create_widgets(self, flag):

        public_key = self.myRsa.public_key.save_pkcs1()
        private_key = self.myRsa.private_key.save_pkcs1()
        if not flag:
            labelTitle = "请保存如下密钥，切勿告知他人!"
            publicTitle = "复制公钥"
            privateTitle = "复制私钥"

        else:
            labelTitle = "请输入原始密钥，切勿告知他人！"
            publicTitle = "粘贴公钥"
            privateTitle = "粘贴私钥"

        Label(self.master).pack()
        self.label = tk.Label(self.master, text=labelTitle, font=self.ft2)
        self.label.pack(pady=8, padx=5)
        Label(self.master, text="公钥", font=self.ft).pack(pady=5)
        self.text = tk.Text(self.master, width=65, height=4, font=self.ft)
        self.text.pack(pady=8)
        self.text.insert(INSERT, public_key.strip())
        Label(self.master, text="私钥", font=self.ft).pack(pady=5)
        self.text2 = tk.Text(self.master, width=65, height=9, font=self.ft)
        self.text2.pack(pady=8)
        self.text2.insert(INSERT, private_key.strip())
        # self.entry.config(state="disabled")
        self.frame = Frame(self.master)
        self.copyPublic = Button(self.frame, text=publicTitle,
                                 command=lambda: self.copyPubicToBoard() if not flag else self.pasteToBoard())
        self.copyPrivate = Button(self.frame, text=privateTitle,
                                  command=lambda: self.copyPrivateToBoard() if not flag else self.pasteToBoard())
        self.exit = Button(self.frame, text="确认", command=self.confirm)
        self.frame.pack(padx=10, pady=10)
        self.copyPublic.pack(side=tk.LEFT, padx=25)
        self.copyPrivate.pack(side=tk.LEFT, padx=25)
        self.exit.pack(side=tk.LEFT, padx=25)

    def login_break(self):
        self.master.destroy()
        self.master.quit()
        sys.exit()

    def confirm(self):
        if self.text.get(1.0, END).strip() == '':
            emptyKey()
            return
        self.myRsa.save_rsa("./resource")
        logger.info("密钥生成成功")
        self.master.destroy()
        self.master.quit()

    def copyPubicToBoard(self):
        # self.copyButton.config(text="粘贴")
        self.master.clipboard_clear()
        self.master.clipboard_append(self.text.get(1.0, END))
        self.label.config(text="复制公钥成功，请妥善保管勿将密钥告知他人!")

    def pasteToBoard(self):
        key = self.master.clipboard_get()
        self.text.delete(1.0, END)
        self.text.insert(1.0, key)
        self.label.config(text="粘贴成功，请妥善保管勿将密钥告知他人!")

    def copyPrivateToBoard(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.text2.get(1.0, END))
        self.label.config(text="复制私钥成功，请妥善保管勿将密钥告知他人!")
