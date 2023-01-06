import tkinter.constants as constants


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
