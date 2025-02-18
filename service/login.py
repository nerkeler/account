import logging, pyautogui
import tkinter as tk
from tkinter import LEFT, RIGHT, END
from tkinter.ttk import *

from dao.baseMapper import BaseDb
from service.updatePassword import UpdatePwd
from utils.bcrypt_util import check_password
from utils.logUtil import setup_logging
from utils.message import loginError
import sys

setup_logging()
logger = logging.getLogger('server')  # 维护一个全局日志对象


class LoginForm:
    def __init__(self, ):

        self.master = tk.Tk()
        self.master.withdraw()  # 隐藏闪烁
        self.master.update()
        self.master.title("登录")
        self.master.resizable(False, False)
        self.master.iconbitmap("./image/account.ico")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        # 不同分辨率/屏幕比例适配
        self.regulators = 1
        self.resolution_ratio = 1
        if float(screen_width / screen_height) == float(16 / 10):
            self.regulators = 1.1
            self.resolution_ratio = screen_height / 800
        elif float(screen_width / screen_height) == float(16 / 9):
            self.regulators = 1
            self.resolution_ratio = screen_height / 720
        w = screen_width / 5 / self.resolution_ratio
        h = screen_height / 3.6 / self.resolution_ratio
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2

        self.master.geometry(
            "%dx%d+%d+%d" % (w / self.regulators * (1 + (self.resolution_ratio - 1) / 2), h / self.regulators * (1 + (self.resolution_ratio - 1) / 4), x, y))

        self.master.deiconify()
        self.base = BaseDb()
        self.master.protocol("WM_DELETE_WINDOW", self.login_break)
        self.create_widgets()

    def create_widgets(self):

        # Label(self.master, text="本地密码保存小工具").pack(pady=5)
        Label(self.master, ).pack(pady=8 / self.regulators)
        nameLabel = Frame(self.master)
        self.username_label = Label(nameLabel, text="用户名称:", )
        self.username_label.pack(side=LEFT)

        self.username_entry = Entry(nameLabel, )
        self.username_entry.insert(END, "admin")
        # self.username_entry.config(state="readonly")
        self.username_entry.pack(side=RIGHT)
        nameLabel.pack(pady=10)

        passwordLabel = Frame(self.master)
        self.password_label = Label(passwordLabel, text="账号密码:")
        self.password_label.pack(side=LEFT)

        self.password_entry = Entry(passwordLabel, show="*")

        self.password_entry.pack(side=RIGHT)
        passwordLabel.pack(pady=10)

        buttonLabel = Frame(self.master)

        self.alter_button = Button(buttonLabel, width=10, text="改密", command=self.update_password)
        self.alter_button.pack(side=LEFT, padx=20)
        self.login_button = Button(buttonLabel, width=10, text="登录", command=lambda: self.login(event=''))
        self.login_button.pack(side=RIGHT)
        self.password_entry.bind("<Return>", self.login)
        buttonLabel.pack(pady=5, padx=20)
        self.password_entry.focus_set()
        self.switch_to_english()  # 切换英文输入法

    def login(self, event):
        username = self.username_entry.get()
        password = self.password_entry.get()
        logger.info(f'用户{username}登录了系统')
        # password = encode_user(password)

        result = self.base.queryOne("1").fetchone()

        if check_password(username, result[1]) and check_password(password, result[2]):
            self.master.destroy()
            self.master.quit()

        else:
            loginError()
            self.password_entry.delete(0, END)
            logger.warning(f"用户{username} 登录错误，用户名或密码错误")

    def login_break(self):
        self.master.destroy()
        self.master.quit()
        sys.exit()

    def update_password(self):
        self.master.iconify()
        updatePass = UpdatePwd()
        updatePass.master.mainloop()
        self.master.state("normal")
        self.password_entry.focus_set()

    def switch_to_english(self):
        try:
            pyautogui.hotkey("ctrl", "space")

        except Exception as e:
            logger.info(f"输入法切换失败：{e}")
