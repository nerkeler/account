import tkinter as tk
from tkinter.ttk import *
from message import loginError, loginSuccess

class LoginForm:
    def __init__(self, ):
        self.master = tk.Tk()
        self.master.title("登录")
        self.master.resizable(False, False)
        self.master.iconbitmap("./image/account.ico")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = 300
        h = 180
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.create_widgets()

    def create_widgets(self):
        self.username_label = Label(self.master, text="用户名:")
        self.username_label.pack()

        self.username_entry = Entry(self.master, )
        self.username_entry.setvar("admin")
        self.username_entry.pack()

        self.password_label = Label(self.master, text="密码:")
        self.password_label.pack()

        self.password_entry = Entry(self.master, show="*")
        self.password_entry.pack()

        self.login_button = Button(self.master, text="登录", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate the login here
        if username == "admin" and password == "password":
            loginSuccess()
            self.master.destroy()
            self.master.quit()
        else:
            loginError()
            self.password_entry.setvar("")



