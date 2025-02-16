import logging
import os
import sqlite3

path1 = "dao"
path2 = "sql"
filename = "account.db"


class Db:

    def __init__(self):
        self.flag = False
        self.check()
        self.connect = sqlite3.connect(f"{path1}/{path2}/{filename}",
                                       detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
                                       isolation_level=None)
        self.connect.text_factory = str
        self.connect.execute('PRAGMA encoding = "UTF-8"')
        self.cur = self.connect.cursor()
        self.init()

    def create_table(self):

        sql_text = '''CREATE TABLE account
                   (id INTEGER primary key AUTOINCREMENT,
                    order_index INTEGER UNIQUE,
                    web_name TEXT,
                    account TEXT,
                    password TEXT,
                    url TEXT,
                    note TEXT,
                    create_time DATETIME not null,
                    update_time DATETIME not null,
                    state INTEGER DEFAULT 1
                   );'''
        self.cur.execute(sql_text)
        logging.info("execute : " + sql_text)

    def insert_account(self, data):
        sql_text = "INSERT INTO account(order_index, web_name, account, password,url, note, create_time, update_time) VALUES(?,?,?,?,?,?,datetime('now'),datetime('now'))"
        row = self.cur.execute(sql_text, data)
        self.connect.commit()
        logging.info("execute : " + sql_text)
        # logging.info("data: ", data)
        return row

    def import_account(self, data):
        sql_text = "INSERT INTO account(web_name,url, account, password, note, order_index, create_time, update_time) VALUES(?,?,?,?,?,?,datetime('now'),datetime('now'))"
        row = self.cur.execute(sql_text, data)
        self.connect.commit()
        logging.info("execute : " + sql_text)
        # logging.info("data: ", data)
        return row

    def update(self, account):
        sql_text = "UPDATE account set web_name=?,account=?, password=?,url=?,note=? where id=?"
        row = self.cur.execute(sql_text, (account[1], account[2], account[3], account[4], account[5], account[0]))
        self.commit()
        logging.info("execute : " + sql_text)
        return row

    def query_url(self, url):

        sql_text = "SELECT order_index,web_name,account,url,note FROM account where state='1'  AND url like'%" + url + "%'  order by order_index"
        logging.info("execute : " + sql_text)
        return self.cur.execute(sql_text)

    def query_all(self):
        query_all = "SELECT order_index,web_name,account,url,note FROM account where state='1' order by order_index"
        accounts = self.cur.execute(query_all).fetchall()
        logging.info("execute : " + query_all)
        return accounts

    def export(self):
        query_all = "SELECT  web_name,url,account,password,note FROM account where state='1'"
        accounts = self.cur.execute(query_all).fetchall()
        logging.info("execute : " + query_all)
        return accounts

    def query_one(self, number):
        sql_text = "SELECT order_index,web_name,account,url,note FROM account where state='1'AND order_index = ? order by order_index"
        logging.info("execute : " + sql_text)
        return self.cur.execute(sql_text, (number,))

    def query_detail(self, number):
        sql_text = "SELECT order_index,web_name,account,password,url,note FROM account where state='1'AND order_index = ?"
        logging.info("execute : " + sql_text)
        return self.cur.execute(sql_text, (number,))

    def query_text(self, text):
        sql_text = "SELECT order_index,web_name,account,url,note FROM account where state='1'  AND web_name like'%" + text + "%'  order by order_index"
        logging.info("execute : " + sql_text)
        return self.cur.execute(sql_text)

    def commit(self):
        self.connect.commit()

    def query_last(self):
        sql_text = "SELECT id,order_index,web_name,account,password,url,note FROM account where state='1'  ORDER BY id DESC limit 1"
        logging.info("execute : " + sql_text)
        return self.cur.execute(sql_text).fetchone()

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
        sql_text = "UPDATE account set state = '0', order_index = (0-order_index) where order_index=?"
        row = self.cur.execute(sql_text, (state,))
        self.commit()
        logging.info("execute : " + sql_text)
        return row

    def up(self, state):
        pre = state - 1
        if state == 1:
            return
        sql_text = "UPDATE account set order_index=0 where order_index=?"
        row1 = self.cur.execute(sql_text, (pre,))
        logging.info("execute : " + sql_text)
        sql_text2 = "UPDATE account set order_index=? where order_index=?"
        row2 = self.cur.execute(sql_text2, (pre, state,))
        logging.info("execute : " + sql_text2)
        sql_text3 = "UPDATE account set order_index = ? where order_index=0"
        row3 = self.cur.execute(sql_text3, (state,))
        logging.info("execute : " + sql_text3)
        self.commit()

    def down(self, state):

        last = self.get_last_index() - 1
        pre = state + 1
        if state == last:
            return

        sql_text = "UPDATE account set order_index=0 where order_index=?"
        row1 = self.cur.execute(sql_text, (pre,))
        logging.info("execute : " + sql_text)
        sql_text2 = "UPDATE account set order_index=? where order_index=?"
        row2 = self.cur.execute(sql_text2, (pre, state,))
        logging.info("execute : " + sql_text2)
        sql_text3 = "UPDATE account set order_index = ? where order_index=0"
        row3 = self.cur.execute(sql_text3, (state,))
        logging.info("execute : " + sql_text3)
        self.commit()

    def get_last_index(self):

        sql_text = "SELECT  order_index  FROM   account where state='1' ORDER  BY  order_index   DESC  LIMIT   1;"

        last_index = 1
        last_index_list = self.cur.execute(sql_text).fetchall()
        if len(last_index_list) == 1:
            last_index = last_index_list[0][0]
            last_index += 1
        logging.info("execute : " + sql_text)
        return last_index
