import hashlib
import tkinter.constants as constants
import rsa
from dao.baseMapper import BaseDb
from utils.MyRSA import MyRSA
from utils.bcrypt_util import encode_password

myRSA = MyRSA()
with open("./resource/public.pem", 'rb') as publickfile:
    pub = publickfile.read()
    PUBLIC = rsa.PublicKey.load_pkcs1(pub)

with open("./resource/private.pem", 'rb') as privatefile:
    priv = privatefile.read()
    PRIVATE = rsa.PrivateKey.load_pkcs1(priv)


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
    default_username = "admin"
    default_password = "password"
    username = encode_password(default_username)
    password = encode_password(default_password)
    baseDb.defaultUser([username, password])


def encode_user(password):
    password = hashlib.md5((password + "slot").encode("utf-8")).hexdigest().__str__()
    password = hashlib.sha3_256(password.encode("utf-8")).hexdigest().__str__()
    return password
