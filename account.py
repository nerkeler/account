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


# 打包命令： pyinstaller -D .\account.py -i .\image\account.ico -w -p .\accountMapper.py -p .\login.py -p .\mainFrame.py -p  .\newAccount.py  -p .\tkConfig.py -p .\updateAccount.py  -p framUtil.py -p message.py
"""
TODO:
    1、启动密钥生成得时候，增加  已有密钥 + 确认按钮  用于更新应用频繁得数据导入
    2、csv 格式导出，只处理account sql 
    3、csv 格式导入，只处理account sql 追加插入数据 需要验证原密钥
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
