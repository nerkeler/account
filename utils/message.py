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


def deleteFailed():
    tkinter.messagebox.showinfo(title="提示", message="删除失败！")


def importSuccess():
    tkinter.messagebox.showinfo(title="提示", message="导入成功！")


def importFailed(e):
    tkinter.messagebox.showinfo(title="提示", message=f"导入失败！{e}")


def loginSuccess():
    tkinter.messagebox.showinfo(title="提示", message="登录成功！")


def loginError():
    tkinter.messagebox.showinfo(title="提示", message="密码错误，请重试！ ")


def keyOrPasswordError():
    tkinter.messagebox.showinfo(title="提示", message="密钥或密码错误，请重试！ ")


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
    return tkinter.messagebox.askokcancel(title="删除账户", message="是否删除当前选中账户？")


def haveKey():
    tkinter.Tk().withdraw()
    return tkinter.messagebox.askquestion(title="创建密钥", message="是否持有密钥用于更新程序？")


def emptyKey():
    tkinter.messagebox.showinfo(title="提示", message="密钥为空")


def exportSuccess():
    tkinter.messagebox.showinfo(title="提示", message="导出成功")
