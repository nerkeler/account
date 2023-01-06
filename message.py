import tkinter.messagebox
from tkinter import *


def noAccount():
    tkinter.messagebox.showinfo(title="提示", message="当前账户编号无数据")


def saveSuccess():
    tkinter.messagebox.showinfo(title="提示", message="保存成功！")

def updateSuccess():
    tkinter.messagebox.showinfo(title="提示", message="更新成功！")
