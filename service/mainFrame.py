import sys
import uuid
from tkinter import *
import tkinter as tk
from tkinter.ttk import *

from dao.accountMapper import Db
from service.newAccount import AddGui
from service.passwordFrame import PasswordFrame
from service.updateAccount import UpdateGui

from utils.framUtil import *
from utils.message import noAccount, deleteSuccess, makeSure
from utils.myAES import decode_password


def drop_func():
    options = ["网站名称", "账户编号", "网站网址"]
    selected_option = StringVar()
    selected_option.set(options[0])
    return options, selected_option


class Gui:
    def __init__(self):
        self.master = tk.Tk()
        self.master.withdraw()  # 隐藏闪烁
        self.master.update()
        self.master.title("账户密码管理器")
        self.master.resizable(False, False)
        self.master.iconbitmap("./image/account.ico")
        options, selected_option = drop_func()
        self.frame = tk.Frame(self.master, )
        self.entry = Entry(self.frame, width=20, )
        self.add_button = Button(self.frame, text="新增", command=self.add_account)
        self.treeFrame = tk.Frame(self.master, bd=8)
        self.tree = Treeview(self.treeFrame, height=50, columns=("网站", "账号", "密码", "网址"))
        self.db = Db()
        self.event = None
        self.tree.bind("<Button-1>", self.showId)
        self.tree.bind("<Double-Button-1>", self.doubleClick)
        self.tree.bind("<Button-3>", self.rightButton)
        self.tree.tag_configure("evenColor", background="lightblue")
        self.dropDown = Combobox(self.frame, textvariable=selected_option, values=options, width=10, state="readonly")
        self.select_button = Button(self.frame, text="查询", command=self.query)
        self.see_button = Button(self.frame, text="查看", command=lambda: self.doubleClick(self.event))
        self.delete_button = Button(self.frame, text="删除", command=self.delete_item)
        self.generate_button = Button(self.frame, text="随机密码", command=self.generate_password)
        self.master.protocol("WM_DELETE_WINDOW", self.login_break)
        self.tk_init()

    def tk_init(self):
        self.show()  # 启动位置
        self.pack()  # 布局
        self.head()  # 设置TreeView head
        self.column()  # 设置TreeView column

    def showAll(self):
        print("首页查询展示")
        accounts = self.db.query_all()
        insert_all(self.tree, accounts)

    # 查询函数
    def query(self):
        print("query开始执行")
        if self.dropDown.get() == "账户编号":
            index = self.entry.get()
            if index.isdigit():
                account = self.db.query_one(index).fetchone()
                if account is None:
                    noAccount()
                else:
                    delete_all(self.tree)
                    insert(self.tree, account)
            else:
                self.reload()
        elif self.dropDown.get() == "网站名称":
            text = self.entry.get()
            accounts = self.db.query_text(text)
            delete_all(self.tree)
            insert_all(self.tree, accounts)

        elif self.dropDown.get() == "网站网址":
            url = self.entry.get()
            accounts = self.db.query_url(url)
            delete_all(self.tree)
            insert_all(self.tree, accounts)

    def doubleClick(self, event):
        if event is not None:
            e = event.widget
            iid = e.identify("item", event.x, event.y)
            state = e.item(iid, "text")
            if state is not None and state != '':
                update = UpdateGui(self.master)
                item = list(self.db.query_one(state).fetchone())
                item[3] = decode_password(item[3])
                update.tk_init(item)
        self.reload()

    def showId(self, event):
        self.event = event

    def delete_item(self):

        if makeSure():
            if self.event is not None:
                print("开始删除")
                e = self.event.widget
                iid = e.identify("item", self.event.x, self.event.y)
                state = e.item(iid, "text")
                print(state)
                row = self.db.delete_one(state).rowcount
                if row == 1:
                    deleteSuccess()
                    self.reload()
        else:
            pass

    def rightButton(self, event):
        menu = self.method_name()
        menu.post(event.x_root, event.y_root)

    def method_name(self):
        menu = Menu(self.master, tearoff=False)
        menu.add_command(label="添加", command=self.add_account)
        menu.add_command(label="删除", command=self.delete_one)
        menu.add_command(label="查看", command=self.doubleClick)
        menu.add_command(label="退出", command=self.master.quit)
        return menu

    def reload(self):
        delete_all(self.tree)
        self.showAll()

    # 添加按钮功能函数
    def add_account(self):
        print("开始新增账号")
        add_gui = AddGui(self.master)
        add_gui.tk_init()
        print("新增框已退出，开始查询插入的数据")
        self.reload()

    def pack(self):
        self.frame.pack()
        self.dropDown.pack(side=LEFT, padx=8, pady=8)
        self.entry.pack(side=LEFT, padx=10, pady=10)
        self.select_button.pack(side=LEFT, padx=8, pady=8)
        self.see_button.pack(side=LEFT, padx=8, pady=8)
        self.add_button.pack(side=LEFT, padx=8, pady=8)
        self.delete_button.pack(side=LEFT, padx=8, pady=8)
        self.generate_button.pack(side=LEFT, padx=8, pady=8)
        self.treeFrame.pack()
        self.tree.pack()

    def show(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = 820
        h = 548
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.deiconify()

    def column(self):
        self.tree.column("#0", width=50, anchor=CENTER)
        self.tree.column("#1", width=188, anchor=CENTER)
        self.tree.column("#2", width=188, anchor=CENTER)
        self.tree.column("#3", width=188, anchor=CENTER)
        self.tree.column("#4", width=188, anchor=CENTER)

    def head(self):
        self.tree.heading("#0", text="序号")
        self.tree.heading("#1", text="网站")
        self.tree.heading("#2", text="账号")
        self.tree.heading("#3", text="密码")
        self.tree.heading("#4", text="网址")

    def login_break(self):
        print("手动关闭窗口了")
        self.master.destroy()
        self.master.quit()
        sys.exit()

    def generate_password(self):
        passwordFrame = PasswordFrame(self.master)
        passwordFrame.master.mainloop()
