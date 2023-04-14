import os
import uuid
from config import tkConfig
from service.keyFrame import KeyFrame
from service.login import LoginForm
from service.mainFrame import Gui
from utils.framUtil import userInit
from utils.message import haveKey


def check_aes():
    # 生成密钥
    if not os.path.exists("resource"):
        os.mkdir("resource")
    if not os.path.exists("resource/aesKey"):
        if haveKey() == "yes":
            keyFrame = KeyFrame(True)
        else:
            keyFrame = KeyFrame(False)
        keyFrame.master.mainloop()
        userInit()  # 默认账号密码


# 打包命令：pyinstaller -D .\account.py -i .\image\account.ico -w -p .\dao\accountMapper.py -p .\dao\baseMapper.py
# -p .\service\keyFrame.py -p .\service\login.py -p .\service\mainFrame.py -p .\service\newAccount.py
# -p .\service\passwordFrame.py -p .\service\updatePassword.py  -p .\service\updateAccount.py -p .\config\tkConfig.py
# -p .\utils\framUtil.py -p .\utils\message.py -p .\utils\myAES.py  -p .\utils\MyRSA.py -p .\utils\reatest.py
"""
TODO:
    1、导出验证密钥和密码
    2、导入标签分三个  本地导入、chrome导入、edge导入和验证
    3、完成chrome导入、edge导入
"""
if __name__ == '__main__':

    # 是否第一次登录，生成密钥
    check_aes()

    login = LoginForm()
    login.master.mainloop()  # 登录验证

    gui = Gui()
    tkConfig.styles(gui)  # 设置样式
    gui.showAll()  # 展示首页
    gui.master.mainloop()  # 主循环
