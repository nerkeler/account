import sys
import tkinter as tk
import tkinter.messagebox
from tkinter.ttk import *
from tkinter import LEFT, RIGHT, END
from dao.baseMapper import BaseDb
from utils.bcrypt_util import encode_password, check_password
from utils.framUtil import encode_user
from utils.message import updateSuccess, pwdNotEqual, pwdError, pwdTooShot, pwdUpdate


class UpdatePwd:
    def __init__(self, ):
        self.master = tk.Tk()
        self.master.withdraw()  # 隐藏闪烁
        self.master.update()
        self.master.title("修改密码")
        self.master.resizable(False, False)
        self.master.iconbitmap("./image/account.ico")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = 280
        h = 230
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.deiconify()
        self.master.protocol("WM_DELETE_WINDOW", self.login_break)
        self.create_widgets()

    def create_widgets(self):
        # Label(self.master, text="本地密码保存小工具").pack(pady=5)
        Label(self.master, ).pack(pady=2)
        self.base = BaseDb()

        nameLabel = Frame(self.master)
        self.username_label = Label(nameLabel, text="原始密码:", )
        self.username_label.pack(side=LEFT)
        self.old_password = Entry(nameLabel, show="*")
        self.old_password.pack(side=RIGHT)
        nameLabel.pack(pady=10)

        passwordLabel = Frame(self.master)
        self.password_label = Label(passwordLabel, text="修改密码:")
        self.password_label.pack(side=LEFT)
        self.new_password = Entry(passwordLabel, show="*")
        self.new_password.pack(side=RIGHT)
        passwordLabel.pack(pady=10)

        passwordConfirmLabel = Frame(self.master)
        self.password_confirm = Label(passwordConfirmLabel, text="确认密码:")
        self.password_confirm.pack(side=LEFT)
        self.confirm_password = Entry(passwordConfirmLabel, show="*")
        self.confirm_password.pack(side=RIGHT)
        passwordConfirmLabel.pack(pady=10)

        buttonLabel = Frame(self.master)
        self.alter_button = Button(buttonLabel, width=10, text="显示", command=self.show)
        self.alter_button.pack(side=LEFT, padx=20)
        self.login_button = Button(buttonLabel, width=10, text="确定", command=self.update_password)
        self.login_button.pack(side=RIGHT)
        buttonLabel.pack(pady=5, padx=20)

    def show(self):

        if self.alter_button.cget("text") == "显示":
            self.old_password.config(show="")
            self.new_password.config(show="")
            self.confirm_password.config(show="")
            self.alter_button.config(text="隐藏")

        else:
            self.old_password.config(show="*")
            self.new_password.config(show="*")
            self.confirm_password.config(show="*")
            self.alter_button.config(text="显示")

    def login_break(self):
        self.master.destroy()
        self.master.quit()

    def update_password(self):
        if tk.messagebox.askquestion(title="提示", message="确认修改？"):
            old_password = self.old_password.get()
            new_password = self.new_password.get()
            confirm_password = self.confirm_password.get()

            result = self.base.queryOne("1").fetchone()

            if len(confirm_password) < 8 or len(new_password) < 8:  # 小于8位密码中断
                pwdTooShot()
                self.new_password.delete(0, END)
                self.confirm_password.delete(0, END)
                return 0
            if not confirm_password == new_password:  # 判断两次新密码是否一致
                pwdNotEqual()

                self.new_password.delete(0, END)
                self.confirm_password.delete(0, END)
                return 0
            if check_password(old_password, result[2]) and confirm_password == new_password:
                new_password = encode_password(new_password)
                if self.base.update([new_password, '1']).rowcount > 0:
                    pwdUpdate()
                    self.master.destroy()
                    self.master.quit()
                    sys.exit()
            else:
                pwdError()
                self.old_password.delete(0, END)
