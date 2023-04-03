import tkinter.messagebox
from tkinter import *


def noAccount():
    tkinter.messagebox.showinfo(title="提示", message="当前账户编号无数据")


def saveSuccess():
    tkinter.messagebox.showinfo(title="提示", message="保存成功！")


def updateSuccess():
    tkinter.messagebox.showinfo(title="提示", message="更新成功！")


def deleteSuccess():
    tkinter.messagebox.showinfo(title="提示", message="删除成功！")


def loginSuccess():
    tkinter.messagebox.showinfo(title="提示", message="登录成功！")


def loginError():
    tkinter.messagebox.showinfo(title="提示", message="密码错误，请重试！ ")


def pwdNotEqual():
    tkinter.messagebox.showinfo(title="提示", message="两次密码输入不一致")


def pwdError():
    tkinter.messagebox.showinfo(title="提示", message="原始密码错误")


def pwdTooShot():
    tkinter.messagebox.showinfo(title="提示", message="密码长度小于8位，请重新输入")


def pwdUpdate():
    tkinter.messagebox.showinfo(title="提示", message="密码更新成功，请重新打开程序！")


def copyPwd():
    tkinter.messagebox.showinfo(title="提示", message="复制成功")


def makeSure():
    return tkinter.messagebox.askokcancel(title="删除账户", message="确定或取消")
