import tkinter as tk
from tkinter.ttk import *
from tkinter import END

choose = {0: "ABC", 1: "abc", 2: "123", 3: "#$&"}


class PasswordFrame:

    def __init__(self):
        self.master = tk.Tk()
        self.master.title("随机密码生成")
        self.master.resizable(False, False)
        self.master.iconbitmap("./image/account.ico")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = 560
        h = 200
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))

        self.generate_frame = Frame(self.master, width=400)
        self.entry = Entry(self.generate_frame, width=30)
        self.generate_button = Button(self.generate_frame, text="生成", command=self.generate)
        self.copy_button = Button(self.generate_frame, text="复制", command=self.copy)
        self.generate_frame.pack(pady=25)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        self.copy_button.pack(side=tk.LEFT, padx=5)

        self.var_ABC = tk.IntVar()
        self.var_abc = tk.IntVar()
        self.var_123 = tk.IntVar()
        self.var_symbol = tk.StringVar()
        self.choose_frame = Frame(self.master, width=400)
        self.choose_label = Label(self.choose_frame, text="所用字符: ")
        self.check_button_ABC = Checkbutton(self.choose_frame, text="ABC", compound=tk.RIGHT, variable=self.var_ABC)
        self.check_button_abc = Checkbutton(self.choose_frame, text="abc", compound=tk.RIGHT, variable=self.var_abc)
        self.check_button_123 = Checkbutton(self.choose_frame, text="123", compound=tk.RIGHT, variable=self.var_123)
        self.check_button_symbol = Checkbutton(self.choose_frame, text="#$&", compound=tk.RIGHT, variable=self.var_symbol)
        self.choose_frame.pack()
        self.choose_label.pack(side=tk.LEFT, padx=22, pady=5)
        self.check_button_ABC.pack(side=tk.LEFT, padx=15, pady=5)
        self.check_button_abc.pack(side=tk.LEFT, padx=15, pady=5)
        self.check_button_123.pack(side=tk.LEFT, padx=15, pady=5)
        self.check_button_symbol.pack(side=tk.LEFT, padx=15, pady=5)

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
        print(self.var_ABC.get())
        print("genearte  running")

    def copy(self):
        print("copy running")

    def printLn(self, event):
        self.scale_label2.config(text=int(self.scale.get()))

