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

