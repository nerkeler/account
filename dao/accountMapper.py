import os
import sqlite3

path1 = "dao"
path2 = "sql"
filename = "account.db"


class Db:

    def __init__(self):
        self.flag = False
        self.check()
        self.connect = sqlite3.connect(f"{path1}/{path2}/{filename}")
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
        row = self.cur.execute(
            "INSERT INTO account(web_name, account, password,url, note, create_time, update_time) VALUES(?,?,?,?,?,datetime('now'),datetime('now'))",
            data)
        self.connect.commit()
        print(f"插入一条数据：{data}")
        return row

    def import_account(self, data):
        row = self.cur.execute(
            "INSERT INTO account(web_name,url, account, password, note, create_time, update_time) VALUES(?,?,?,?,?,datetime('now'),datetime('now'))",
            data)
        self.connect.commit()
        print(f"插入一条数据：{data}")
        return row

    def update(self, account):
        row = self.cur.execute("UPDATE account set web_name=?,account=?, password=?,url=?,note=? where id=?",
                               (account[1], account[2], account[3], account[4], account[5], account[0]))
        self.commit()
        return row

    def query_url(self, url):
        return self.cur.execute(
            "SELECT id,web_name,account,password,url,note FROM account where state='1'  AND url like'%" + url + "%'")

    def query_all(self):
        query_all = "SELECT id,web_name,account,password,url,note FROM account where state='1'"
        accounts = self.cur.execute(query_all).fetchall()
        print("执行查询所有数据")
        return accounts

    def export(self):
        query_all = "SELECT web_name,url,account,password,note FROM account where state='1'"
        accounts = self.cur.execute(query_all).fetchall()
        print("执行查询所有数据")
        return accounts

    def query_one(self, number):
        return self.cur.execute("SELECT id,web_name,account,password,url,note FROM account where state='1'AND id = ?",
                                (number,))

    def query_text(self, text):
        return self.cur.execute(
            "SELECT id,web_name,account,password,url,note FROM account where state='1'  AND web_name like'%" + text + "%'")

    def commit(self):
        self.connect.commit()

    def query_last(self):
        return self.cur.execute("SELECT id,web_name,account,password,url,note FROM account  ORDER BY id DESC limit 1",
                                ).fetchone()

    def init(self):
        if self.flag:
            self.create_table()
            self.commit()

    def check(self):
        if not os.path.exists(path1):
            os.mkdir(path1)
        if not os.path.exists(f'{path1}/{path2}'):
            os.mkdir(f'{path1}/{path2}')
        if not os.path.exists(f"{path1}/{path2}/{filename}"):
            f = open(f"{path1}/{path2}/{filename}", "w")
            f.close()
            self.flag = True

    def delete_one(self, state):
        row = self.cur.execute("UPDATE account set state = '0' where id=?", (state,))
        self.commit()
        return row
