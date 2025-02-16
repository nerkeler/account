import csv
import tkinter as tk
from sqlite3 import ProgrammingError
from tkinter import ttk
from dao.accountMapper import Db
from utils.myAES import encode_password
from utils.message import importFailed, importSuccess


class InputProgressBar:
    def __init__(self, root, folder_path, main_app):
        self.master = tk.Toplevel(master=root)
        self.master.withdraw()  # 隐藏闪烁
        self.master.update()
        self.master.title("关于")
        self.master.resizable(False, False)
        self.master.iconbitmap("./image/account.ico")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        w = screen_width / 3.5
        h = screen_height / 8
        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.deiconify()

        self.main_app = main_app  # 保存主应用的引用
        self.path = folder_path
        self.step_num = self.get_page_num()
        self.progress_var = tk.IntVar()
        self.db = Db()

        # 创建进度条
        self.progress_bar = ttk.Progressbar(self.master, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=20, padx=20, fill=tk.X)

        # 创建进度详细信息标签
        self.progress_label = tk.Label(self.master, text=f"正在进行 第 0 个 / 共 {self.step_num} 个 进度 0%")
        self.progress_label.pack(pady=10)

        # 启动进度条
        self.update_progress()

    def get_page_num(self):

        total_steps = 0

        with open(self.path, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # 跳过第一行
            for _ in reader:
                total_steps += 1
        return total_steps

    def update_progress(self):

        total_steps = self.step_num
        now_step = 0
        order_index = self.db.get_last_index()
        try:
            with open(self.path, "r", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # 跳过第一行
                for i in reader:
                    now_step += 1

                    # 进度条
                    self.progress_var.set(now_step)
                    percentage = int((now_step / total_steps) * 100)
                    self.progress_label.config(
                        text=f"正在进行 第 {now_step} 个 / 共 {total_steps} 个 进度 {percentage}%")
                    self.progress_bar.update()  # 刷新进度条和标签

                    # 写入数据库
                    password = i[3]
                    i[3] = encode_password(password)
                    i.append(order_index)
                    self.db.import_account(i)
                    order_index += 1

                importSuccess()

                self.exit()
        except ProgrammingError as e:
            importFailed(e)

    def exit(self):
        self.master.destroy()
        self.master.quit()
        self.main_app.reload()  # 调用主应用的 reload 方法
