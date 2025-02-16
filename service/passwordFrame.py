import random
import tkinter as tk
from tkinter.ttk import *
from tkinter import END

choose = {0: "ABC", 1: "abc", 2: "123", 3: "#$&"}
constant_all = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&!"
constant_ABC = [chr(i) for i in range(65, 91)]
constant_abc = [chr(i) for i in range(97, 123)]
constant_123 = [chr(i) for i in range(48, 58)]
constant_symbol = [chr(i) for i in range(35, 39)]
constant_symbol.append("!")


class PasswordFrame:

    def __init__(self, root):
        self.master = tk.Toplevel(master=root)
        self.master.withdraw()  # 隐藏闪烁
        self.master.update()
        self.master.title("随机密码生成")
        self.master.resizable(False, False)
        self.master.iconbitmap("./image/account.ico")
        # 使弹出窗口一直处于主窗口前面
        self.master.transient(root)
        # 将top1设置为模式对话框，top1不关闭无法操作主窗口
        self.master.grab_set()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = screen_width / 4
        h = screen_height / 8
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.deiconify()
        self.generate_frame = Frame(self.master, width=400)
        self.entry = Entry(self.generate_frame, width=30)
        self.generate_button = Button(self.generate_frame, text="生成", command=self.generate)
        self.copy_button = Button(self.generate_frame, text="复制", command=self.copy)
        self.generate_frame.pack(pady=25)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        self.copy_button.pack(side=tk.LEFT, padx=5)

        self.choose_frame = Frame(self.master, width=400)
        self.var_ABC = tk.StringVar(master=self.choose_frame, value="1")
        self.var_abc = tk.StringVar(master=self.choose_frame, value="1")
        self.var_123 = tk.StringVar(master=self.choose_frame, value="1")
        self.var_symbol = tk.StringVar(master=self.choose_frame, value="1")
        self.choose_label = Label(self.choose_frame, text="密码字符类型选择: ")
        self.check_button_ABC = Checkbutton(self.choose_frame, text="ABC", compound=tk.RIGHT, variable=self.var_ABC)
        self.check_button_abc = Checkbutton(self.choose_frame, text="abc", compound=tk.RIGHT, variable=self.var_abc)
        self.check_button_123 = Checkbutton(self.choose_frame, text="123", compound=tk.RIGHT, variable=self.var_123)
        self.check_button_symbol = Checkbutton(self.choose_frame, text="#$&", compound=tk.RIGHT,
                                               variable=self.var_symbol)
        self.choose_frame.pack()
        self.choose_label.pack(side=tk.LEFT, padx=22, pady=5)
        self.check_button_ABC.pack(side=tk.LEFT, padx=10, pady=5)
        self.check_button_abc.pack(side=tk.LEFT, padx=10, pady=5)
        self.check_button_123.pack(side=tk.LEFT, padx=10, pady=5)
        self.check_button_symbol.pack(side=tk.LEFT, padx=10, pady=5)

        intVar = tk.IntVar()
        self.scale_frame = Frame(self.master, width=400)
        self.scale_label = Label(self.scale_frame, text="密码长度: ")
        self.scale_label2 = Label(self.scale_frame, text="8")
        self.scale = Scale(self.scale_frame, from_=4, to=30, length=300, orient=tk.HORIZONTAL, variable=intVar,
                           command=self.printLn)

        self.scale.set(8)
        self.scale_frame.pack()
        self.scale_label.pack(side=tk.LEFT, padx=5, pady=5, ipady=10)
        self.scale_label2.pack(side=tk.LEFT, padx=5, pady=5, ipady=10)
        self.scale.pack(side=tk.LEFT, pady=5, padx=5)

        self.master.protocol("WM_DELETE_WINDOW", self.login_break)

    def login_break(self):
        self.master.destroy()
        self.master.quit()

    def generate(self):

        length = int(self.scale.get())
        gen_pass = ''
        if self.var_123.get() == "1":
            gen_pass = gen_pass + ''.join(constant_123)
        if self.var_abc.get() == "1":
            gen_pass = gen_pass + "".join(constant_abc)
        if self.var_ABC.get() == "1":
            gen_pass = gen_pass + ''.join(constant_ABC)
        if self.var_symbol.get() == "1":
            gen_pass = gen_pass + ''.join(constant_symbol)
        if gen_pass == '':
            gen_pass = constant_all
        if length > len(gen_pass):
            for i in range(length - (len(gen_pass)) + 2):
                gen_pass += str(random.randint(0, 10))

        password = ''.join(random.sample(gen_pass, length))
        self.entry.delete(0, END)
        self.entry.insert(0, password)

    def copy(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.entry.get())

    def printLn(self, event):
        self.scale_label2.config(text=int(self.scale.get()))
        self.generate()