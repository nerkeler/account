import csv
import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
from dao.accountMapper import Db
from dao.baseMapper import BaseDb
from utils.bcrypt_util import check_password
from utils.message import exportSuccess, keyOrPasswordError
from utils.myAES import encode_key, encode_password, decode_password


class ExportFileFrame:

    def __init__(self, root):
        self.master = tk.Toplevel(master=root)
        self.master.withdraw()  # 隐藏闪烁
        self.master.update()
        self.master.title("数据导出")
        self.master.resizable(False, False)
        self.master.iconbitmap("./image/account.ico")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = 400
        h = 200
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.deiconify()
        # 将top1设置为模式对话框，top1不关闭无法操作主窗口
        self.master.grab_set()
        # self.master.protocol("WM_DELETE_WINDOW", self.login_break())
        self.create_widgets()

    def create_widgets(self):
        self.label = Label(self.master, text="请在下方输入原始密钥")
        self.label.pack(pady=5, padx=5)

        self.entry = Entry(self.master, width=39)
        self.entry.pack(pady=8)
        self.label = Label(self.master, text="请在下方输入程序密码")
        self.label.pack(pady=5, padx=5)

        self.entry2 = Entry(self.master, width=39, show="*")
        self.entry2.pack(pady=8)
        self.button = Button(self.master, text="确认", command=self.confirm)
        self.button.pack(pady=5, padx=5)

    def confirm(self):
        key = self.entry.get()
        password = self.entry2.get()
        with open("resource/aesKey", encoding='utf-8') as f:
            localKey = f.read().strip()
        baseDb = BaseDb()
        db = Db()
        result = baseDb.queryOne("1").fetchone()
        if localKey == key and check_password(password, result[2]):
            self.master.quit()
            self.master.destroy()
            root = tk.Tk()
            root.withdraw()
            root.iconbitmap("./image/account.ico")
            FolderPath = filedialog.asksaveasfilename(initialdir="/", title="保存文件", initialfile="account.csv",
                                                      filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
            if FolderPath is not None and FolderPath != "":
                accounts = list(db.export())
                exportList = []
                for account in accounts:
                    account = list(account)
                    account[3] = decode_password(account[3])
                    exportList.append(account)
                if FolderPath is not None and FolderPath != '':
                    with open(FolderPath, "w", newline='', encoding="utf-8-sig") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(["名称", "网址", "账号", "密码", "备注"])
                        writer.writerows(exportList)
                exportSuccess()
        else:
            keyOrPasswordError()
            self.entry.delete(0, tk.END)
            self.entry2.delete(0, tk.END)

    def login_break(self):
        self.master.quit()
        self.master.destroy()
