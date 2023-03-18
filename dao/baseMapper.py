import os
import sqlite3

path = "dao/sql"
filename = "user.db"


class BaseDb:
    def __init__(self):
        self.flag = False
        self.check()
        self.connect = sqlite3.connect(f"{path}/{filename}")
        self.cur = self.connect.cursor()
        self.init()

    def init(self):
        if self.flag:
            self.create()

    def create(self):
        sql_text = '''CREATE TABLE user
                           (id INTEGER primary key AUTOINCREMENT,
                            username TEXT,
                            password TEXT,
                            create_time DATETIME not null,
                            update_time DATETIME not null,
                            state INTEGER DEFAULT 1
                           );'''

        self.cur.execute(sql_text)
        self.connect.commit()

    def update(self, item):
        row = self.cur.execute("UPDATE user set password=? where id=?", (item[0],item[1]))
        self.connect.commit()
        return row

    def defaultUser(self, data):
        row = self.cur.execute(
            "INSERT INTO user(username, password,  create_time, update_time) VALUES(?,?,datetime('now'),datetime('now'))",
            data)
        self.connect.commit()
        return row

    def queryOne(self, num):
        return self.cur.execute(
            "SELECT id,username,password FROM user where id = ?",
            (num,))

    def check(self):

        if not os.path.exists(path):
            os.mkdir(path)
            if not os.path.exists(f"{path}/{filename}"):
                f = open(f"{path}/{filename}", "w")
                f.close()
                self.flag = True
