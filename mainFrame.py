from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from newAccount import AddGui
from accountMapper import Db
from updateAccount import UpdateGui


def drop_func():
    options = ["账户编号", "网站名称", "网站网址", "网站备注"]
    selected_option = StringVar()
    selected_option.set(options[0])
    return options, selected_option


def doubleClick(event):
    update = UpdateGui()
    db = Db()
    e = event.widget
    iid = e.identify("item", event.x, event.y)
    state = e.item(iid, "text")
    item = db.query_one(state).fetchone()
    update.tk_init(item)

class Gui:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("账户密码管理器")
        self.master.iconbitmap("./image/account.ico")
        options, selected_option = drop_func()
        self.frame = tk.Frame(self.master)
        self.entry = Entry(self.frame, width=50)
        self.select_button = Button(self.frame, text="查询")
        self.add_button = Button(self.frame, text="新增", command=self.add_account)
        self.treeFrame = tk.Frame(self.master, bd=8)
        self.tree = Treeview(self.treeFrame, height=50, columns=("网站", "账号", "密码", "网址"))
        self.tree.bind("<Double-1>", doubleClick)
        self.tree.tag_configure("evenColor", background="lightblue")
        self.dropDown = Combobox(self.frame, textvariable=selected_option, values=options, width=10, state="readonly")
        self.tk_init()

    def tk_init(self):
        self.show()  # 启动位置
        self.pack()  # 布局
        self.head()  # 设置TreeView head
        self.column()  # 设置TreeView column

    # 插入一行数据
    def insert(self, text, values, tags):
        if tags != '' and tags[0] == "evenColor":
            self.tree.insert("", index=END, text=text, values=values, tags=tags)
        else:
            self.tree.insert("", index=END, text=text, values=values)

    # 添加按钮功能函数
    def add_account(self):
        # self.add_button.configure(state='disabled')
        print("开始新增账号")
        add_gui = AddGui()
        db = Db()
        add_gui.tk_init()
        print("新增框已退出，开始查询插入的数据")
        data = db.query_last()
        account = list(data)
        account[3] = "************"
        print(f"最后一条数据为： {account}")
        self.insert(account[0], account[1:],'')
        # self.add_button.configure(state='normal')

    def pack(self):
        self.frame.pack()
        self.dropDown.pack(side=LEFT, padx=8, pady=8)
        self.entry.pack(side=LEFT, padx=10, pady=10)
        self.select_button.pack(side=LEFT, padx=8, pady=8)
        self.add_button.pack(side=LEFT, padx=8, pady=8)
        self.treeFrame.pack()
        self.tree.pack()

    def show(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = 900
        h = 548
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))

    def column(self):
        self.tree.column("#0", width=50)
        self.tree.column("#1", anchor=CENTER)
        self.tree.column("#2", anchor=CENTER)
        self.tree.column("#3", anchor=CENTER)
        self.tree.column("#4", anchor=CENTER)

    def head(self):
        self.tree.heading("#0", text="序号")
        self.tree.heading("#1", text="网站")
        self.tree.heading("#2", text="账号")
        self.tree.heading("#3", text="密码")
        self.tree.heading("#4", text="网址")



