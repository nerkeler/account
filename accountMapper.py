import os
import sqlite3


class Db:
    def __init__(self):
        self.check()
        self.connect = sqlite3.connect('account.db')
        self.cur = self.connect.cursor()
        self.init()

    def create_table(self):

        sql_text = '''CREATE TABLE account
                   (id INTEGER primary key AUTOINCREMENT,
                    web_name TEXT,
                    account TEXT,
                    password TEXT,
                    url TEXT,
                    note TEXT,
                    create_time DATETIME not null,
                    update_time DATETIME not null,
                    state INTEGER DEFAULT 1
                   );'''
        print("创建account表格成功")
        self.cur.execute(sql_text)

    def insert_account(self, data):
        row = self.cur.execute("INSERT INTO account(web_name, account, password,url, note, create_time, update_time) VALUES(?,?,?,?,?,datetime('now'),datetime('now'))", data)
        self.connect.commit()
        print(f"插入一条数据：{data}")
        return row

    def query_all(self):
        query_all = "SELECT id,web_name,account,password,url,note FROM account where state='1'"
        accounts = self.cur.execute(query_all).fetchall()
        print("执行查询所有数据")
        return accounts

    def query_one(self, number):
        return self.cur.execute("SELECT id,web_name,account,password,url,note FROM account where state='1'AND id = ?", (number,))

    def commit(self):
        self.connect.commit()

    def query_last(self):
        return self.cur.execute("SELECT id,web_name,account,password,note FROM account  ORDER BY id DESC limit 1", ).fetchone()

    def init(self):
        if not os.path.exists("account.db"):
            self.create_table()
            self.commit()

    def check(self):
        if not os.path.exists("account.db"):
            f = open("account.db", "w")
            f.close()


