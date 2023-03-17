import hashlib
import tkinter.constants as constants

from dao.baseMapper import BaseDb
from utils.myAES import encode_password


# 插入一行数据
def insert(tree, account):
    account = list(account)
    account[3] = "************"
    tree.insert("", index=constants.END, text=account[0], values=account[1:])


def insert_all(tree, items):
    for account in items:
        insert(tree, account)


def delete_all(tree):
    for item in tree.get_children():
        tree.delete(item)


def userInit():
    # 生成默认账号
    baseDb = BaseDb()
    default_password = "password"
    password = encode_user(default_password)
    baseDb.defaultUser(["admin", password])


def encode_user(password):
    password = hashlib.md5((password+"slot").encode("utf-8")).hexdigest().__str__()
    password = hashlib.sha3_256(password.encode("utf-8")).hexdigest().__str__()
    return password
