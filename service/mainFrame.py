import csv
import logging
import sys
import ctypes
from sqlite3 import ProgrammingError
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter.ttk import *
from tkinter import font
from dao.accountMapper import Db
from service.about import FunctionIntroPag
from service.exportFileFrame import ExportFileFrame
from service.newAccount import AddGui
from service.passwordFrame import PasswordFrame
from service.updateAccount import UpdateGui

from utils.framUtil import *
from utils.logUtil import setup_logging
from utils.message import noAccount, deleteSuccess, makeSure, deleteFailed, importFailed, importSuccess
from utils.myAES import decode_password

setup_logging()
logger = logging.getLogger('server')  # 维护一个全局日志对象


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
        self.ft = font.Font(family='Consolas', size=13)  # 设置出文本框字体
        options, selected_option = drop_func()
        self.menubar = Menu(self.master)
        self.importMenu = Menu(self.menubar, tearoff=False)
        self.menubar.add_command(label="首页", command=self.reload)
        self.menubar.add_cascade(label="导入", menu=self.importMenu)
        self.importMenu.add_command(label="本地导入", command=self.importFile, accelerator="Ctrl+A")
        self.importMenu.add_separator()
        self.importMenu.add_command(label="chrome导入", command=self.chromeImportFile, accelerator='Ctrl+S')
        self.importMenu.add_command(label="edge导入", command=self.edgeImportFile, accelerator="Ctrl+D")
        self.menubar.add_command(label="导出", command=self.export)
        self.menubar.add_command(label="关于", command=self.bout)
        self.master.bind("<Control-A>", lambda event: self.importFile())
        self.master.bind("<Control-S>", lambda event: self.chromeImportFile())
        self.master.bind("<Control-D>", lambda event: self.edgeImportFile())
        self.master.config(menu=self.menubar)
        self.frame = Frame(self.master, relief="flat")
        self.treeFrame = Frame(self.master, borderwidth=0, relief="solid")
        self.tree = Treeview(self.treeFrame, height=50,  columns=("网站", "账号", "密码", "网址"))
        self.VScroll1 = Scrollbar(self.treeFrame, command=self.tree.yview)
        self.tree.config(yscrollcommand=self.VScroll1.set)
        self.VScroll1.config(orient="vertical")
        self.db = Db()
        self.event = None
        self.tree.bind("<Button-1>", self.showId)
        self.tree.bind("<Double-Button-1>", self.doubleClick)
        # self.tree.bind("<Button-3>", self.rightButton)
        self.tree.tag_configure("evenColor", background="lightblue")
        self.dropDown = Combobox(self.frame, textvariable=selected_option, values=options, width=10, state="readonly")
        self.entry = Entry(self.frame, width=27)
        self.entry.bind("<Return>", self.query)
        self.select_button = Button(self.frame, text="查询", command=lambda: self.query(event=""))
        self.see_button = Button(self.frame, text="查看", command=lambda: self.doubleClick(self.event))
        self.add_button = Button(self.frame, text="新增", command=self.add_account)
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
        logger.info("首页查询展示")
        accounts = self.db.query_all()
        insert_all(self.tree, accounts)

    # 查询函数
    def query(self, event):
        logger.info("query开始执行")
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
            flag = True
            if self.event is not None:
                logger.info("开始删除")
                e = self.event.widget
                selected_items = self.tree.selection()
                for iid in selected_items:
                    state = e.item(iid, "text")
                    row = self.db.delete_one(state).rowcount
                    if row != 1:
                        flag = False

                if flag:
                    deleteSuccess()
                else:
                    deleteFailed()
                self.reload()
        else:
            pass

    def rightButton(self, event):
        menu = self.method_name()
        menu.post(event.x_root, event.y_root)

    def method_name(self):
        menu = Menu(self.master, tearoff=False)
        menu.add_command(label="添加", command=self.add_account)
        # menu.add_command(label="删除", command=self.delete_one)
        menu.add_command(label="查看", command=self.doubleClick)
        menu.add_command(label="退出", command=self.master.quit)
        return menu

    def reload(self):
        delete_all(self.tree)
        self.showAll()

    # 添加按钮功能函数
    def add_account(self):
        logger.info("开始新增账号")
        add_gui = AddGui(self.master)
        add_gui.tk_init()
        self.reload()

    def pack(self):
        self.frame.pack(side="top", )
        self.dropDown.pack(side=LEFT, padx=8, pady=8)
        self.entry.pack(side=LEFT, padx=10, pady=10)
        self.select_button.pack(side=LEFT, padx=8, pady=8)
        self.see_button.pack(side=LEFT, padx=8, pady=8)
        self.add_button.pack(side=LEFT, padx=8, pady=8)
        self.delete_button.pack(side=LEFT, padx=8, pady=8)
        self.generate_button.pack(side=LEFT, padx=8, pady=8)
        self.treeFrame.pack(side="top", pady=5)
        self.tree.pack(side="left", fill="y")
        self.VScroll1.pack(side="right", fill="y")

    def show(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = 850
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
        logger.info("手动关闭窗口了")
        self.master.destroy()
        self.master.quit()
        sys.exit()

    def generate_password(self):
        passwordFrame = PasswordFrame(self.master)
        passwordFrame.master.mainloop()

    def export(self):
        exportFile = ExportFileFrame(self.master)
        exportFile.master.mainloop()

    def importFile(self):
        root = tk.Tk()
        root.withdraw()
        root.title("数据导入")
        root.iconbitmap("./image/account.ico")
        FolderPath = filedialog.askopenfilename(initialdir="/", title="数据导入",
                                                filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        if FolderPath is None or FolderPath == '':
            return
        try:
            with open(FolderPath, "r", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # 跳过第一行
                for i in reader:
                    password = i[3]
                    i[3] = encode_password(password)
                    row = self.db.import_account(i)

                importSuccess()
        except ProgrammingError as e:
            importFailed(e)

        self.reload()

    def bout(self):

        function_intro_page = FunctionIntroPag(self.master)
        function_intro_page.master.mainloop()

    def chromeImportFile(self):
        self.importFile()

    def edgeImportFile(self):
        root = tk.Tk()
        root.withdraw()
        root.title("Edge数据导入")
        root.iconbitmap("./image/account.ico")
        FolderPath = filedialog.askopenfilename(initialdir="/", title="Edge数据导入",
                                                filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        if FolderPath is None or FolderPath == '':
            return
        try:
            with open(FolderPath, "r", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # 跳过第一行
                for i in reader:
                    password = i[3]
                    i[3] = encode_password(password)
                    row = self.db.edge_import(i).fetchone()

                importSuccess()
        except ProgrammingError as e:
            importFailed(e)

        self.reload()
