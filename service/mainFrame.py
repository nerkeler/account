import logging
import sys

import tkinter as tk
from tkinter import filedialog, font
from tkinter.ttk import *

from dao.accountMapper import Db

from service.InputProgressBar import InputProgressBar
from service.about import FunctionIntroPag
from service.exportFileFrame import ExportFileFrame
from service.newAccount import AddGui
from service.passwordFrame import PasswordFrame
from service.updateAccount import UpdateGui

from utils.framUtil import insert_all, delete_all, insert
from utils.logUtil import setup_logging
from utils.message import noAccount, deleteSuccess, makeSure, deleteFailed
from utils.myAES import decode_password

setup_logging()
logger = logging.getLogger('server')  # 维护一个全局日志对象


class Gui:
    def __init__(self):

        self.master = tk.Tk()
        self.master.withdraw()  # 隐藏闪烁
        self.master.update()
        self.master.title("账户密码管理器")
        # self.master.resizable(False, False)
        self.master.iconbitmap("./image/account.ico")
        self.show()  # 启动位置

        # 配置
        self.ft = font.Font(family='Consolas', size=13)  # 设置出文本框字体
        self.options, self.selected_option = self.drop_func()
        self.db = Db()

        # menubar
        self.menubar = tk.Menu(self.master)
        self.menubar.add_cascade(label="首页", command=self.reload)

        self.home = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="导入导出", menu=self.home)

        self.home.add_command(label="本地导入", command=self.import_file, accelerator="Alt+A")

        self.importMenu = tk.Menu(self.menubar, tearoff=False)
        self.home.add_cascade(label="浏览器导入", menu=self.importMenu)
        self.importMenu.add_command(label="chrome导入", command=self.chrome_import_file, accelerator='Alt+S')
        self.importMenu.add_command(label="edge导入", command=self.edge_import_file, accelerator="Alt+D")

        self.home.add_separator()

        self.home.add_command(label="本地导出", command=self.export)
        self.menubar.add_cascade(label="密码生成器", command=self.generate_password)

        self.aboutMenu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="关于", menu=self.aboutMenu)
        self.aboutMenu.add_command(label="about", command=self.bout)

        # 快捷键绑定
        self.master.bind("<Alt-A>", lambda event: self.import_file())
        self.master.bind("<Alt-S>", lambda event: self.chrome_import_file())
        self.master.bind("<Alt-D>", lambda event: self.edge_import_file())
        self.master.config(menu=self.menubar)

        # 主体
        self.frame = Frame(self.master, relief="flat", height=int(self.h * 0.2), width=self.w)
        self.event = None

        # 按键行
        self.dropDown = Combobox(self.frame, textvariable=self.selected_option, values=self.options, width=10,
                                 state="readonly")
        self.entry = Entry(self.frame, width=25)
        self.entry.bind("<Return>", self.query)

        self.select_button = Button(self.frame, text="查询", command=lambda: self.query(event=""))
        # self.see_button = Button(self.frame, text="查看", command=lambda: self.doubleClick(self.event))
        self.add_button = Button(self.frame, text="新增", command=self.add_account)
        self.delete_button = Button(self.frame, text="删除", command=self.delete_item)
        self.up_button = Button(self.frame, text="上移", command=self.up)
        self.down_button = Button(self.frame, text="下移", command=self.down)

        # 展示行
        self.treeFrame = Frame(self.master, borderwidth=0, relief="solid")
        self.tree = Treeview(self.treeFrame, height=int(self.h * 0.7), columns=("网站", "账号", "网址"))

        self.VScroll1 = Scrollbar(self.treeFrame, command=self.tree.yview)
        self.tree.config(yscrollcommand=self.VScroll1.set)
        self.VScroll1.config(orient="vertical")

        self.tree.bind("<Button-1>", self.showId)
        self.tree.bind("<Double-Button-1>", self.doubleClick)
        # self.tree.bind("<Button-3>", self.rightButton)

        self.master.protocol("WM_DELETE_WINDOW", self.login_break)
        self.tk_init()

    def tk_init(self):
        self.pack()  # 布局
        self.head()  # 设置TreeView head
        self.column()  # 设置TreeView column

    def showAll(self):
        logger.info("首页查询展示")
        accounts = self.db.query_all()
        insert_all(self.tree, accounts)

    def drop_func(self):
        options = ["网站名称", "账户编号", "网站网址"]
        selected_option = tk.StringVar()
        selected_option.set(options[0])
        return options, selected_option

    def showId(self, event):
        self.event = event

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
                item = list(self.db.query_detail(state).fetchone())
                item[3] = decode_password(item[3])
                update.tk_init(item)
        self.reload()

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
        menu = tk.Menu(self.master, tearoff=False)
        menu.add_command(label="添加", command=self.add_account)
        # menu.add_command(label="删除", command=self.delete_one)
        menu.add_command(label="查看", command=lambda: self.doubleClick)
        menu.add_command(label="退出", command=self.master.quit)
        return menu

    def reload(self):
        delete_all(self.tree)
        self.showAll()

    # 添加按钮功能函数
    def add_account(self):
        # logger.info("开始新增账号")
        add_gui = AddGui(self.master)
        add_gui.tk_init()
        self.reload()

    def pack(self):
        self.frame.pack(side="top", )
        self.dropDown.pack(side=tk.LEFT, padx=8, pady=8)
        self.entry.pack(side=tk.LEFT, padx=10, pady=10)
        self.select_button.pack(side=tk.LEFT, padx=8, pady=8)
        # self.see_button.pack(side=tk.LEFT, padx=8, pady=8)
        self.add_button.pack(side=tk.LEFT, padx=8, pady=8)
        self.delete_button.pack(side=tk.LEFT, padx=8, pady=8)
        self.up_button.pack(side=tk.LEFT, padx=8, pady=8)
        self.down_button.pack(side=tk.LEFT, padx=8, pady=8)
        self.treeFrame.pack(side="top", pady=5)
        self.tree.pack(side="left", fill="y")
        self.VScroll1.pack(side="right", fill="y")

    def show(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.w = screen_width / 2
        self.h = screen_height / 2
        x = (screen_width - self.w) / 2
        y = (screen_height - self.h) / 2
        self.master.geometry("%dx%d+%d+%d" % (self.w - 80, self.h, x, y))
        self.master.deiconify()

    def column(self):
        part_col = int(self.w / 20)
        self.tree.column("#0", width=part_col * 1, anchor="w")
        self.tree.column("#1", width=part_col * 5, anchor="w")
        self.tree.column("#2", width=part_col * 5, anchor="w")
        self.tree.column("#3", width=part_col * 7, anchor="w")

    def head(self):
        self.tree.heading("#0", text="序号")
        self.tree.heading("#1", text="网站")
        self.tree.heading("#2", text="账号")
        self.tree.heading("#3", text="网址")

    def login_break(self):
        logger.info("手动关闭窗口了")
        self.master.destroy()
        self.master.quit()
        sys.exit()

    def generate_password(self):
        passwordFrame = PasswordFrame(self.master)
        passwordFrame.master.mainloop()

    def export(self):
        export_file = ExportFileFrame(self.master)
        export_file.master.mainloop()

    def up(self):
        target = 0
        if self.event is not None:
            logger.info("上移一位")
            e = self.event.widget
            selected_items = self.tree.selection()
            for iid in selected_items:
                state = e.item(iid, "text")
                target = state
                # print(state)
                self.db.up(state)
            self.reload()
            self.traverse_treeview(self.tree, None, target - 1)

    def down(self):
        target = 0
        if self.event is not None:
            logger.info("下移一位")
            e = self.event.widget
            selected_items = self.tree.selection()
            for iid in selected_items:
                state = e.item(iid, "text")
                target = state
                # print(state)
                self.db.down(state)
            self.reload()
            self.traverse_treeview(self.tree, None, target + 1)

    def traverse_treeview(self, tree: Treeview, child=None, target=0):
        items = tree.get_children(child)
        for item in items:

            state = self.event.widget.item(item, "text")
            if state == target:
                self.tree.selection_set(item)

            self.traverse_treeview(tree, item)

    def import_file(self):
        root = tk.Tk()
        root.withdraw()
        root.title("数据导入")
        root.iconbitmap("./image/account.ico")
        folder_path = filedialog.askopenfilename(initialdir="Users/Public/Desktop", title="数据导入",
                                                 filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        if folder_path is None or folder_path == '':
            return
        bar = InputProgressBar(self.master, folder_path, self)
        bar.master.mainloop()

    def bout(self):

        function_intro_page = FunctionIntroPag(self.master)
        function_intro_page.master.mainloop()

    def chrome_import_file(self):
        self.import_file()

    def edge_import_file(self):
        root = tk.Tk()
        root.withdraw()
        root.title("Edge数据导入")
        root.iconbitmap("./image/account.ico")
        folder_path = filedialog.askopenfilename(initialdir="/", title="Edge数据导入",
                                                 filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        if folder_path is None or folder_path == '':
            return
        bar = InputProgressBar(self.master, folder_path, self)
        bar.master.mainloop()
