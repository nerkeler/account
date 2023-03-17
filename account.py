import os
import uuid
from config import tkConfig
from service.keyFrame import KeyFrame
from service.login import LoginForm
from service.mainFrame import Gui
from utils.framUtil import userInit


def check_aes():
    # 生成密钥
    if not os.path.exists("resource/aesKey"):
        key = uuid.uuid4().__str__()
        with open('resource/aesKey', 'w', encoding='utf-8') as f:  # 使用with open()新建对象f
            f.write(key)
        keyFrame = KeyFrame(key)
        keyFrame.master.mainloop()
        # 生成默认账号
        userInit()


# 打包命令： pyinstaller -D .\account.py -i .\image\account.ico -w -p .\accountMapper.py -p .\login.py -p .\mainFrame.py -p  .\newAccount.py  -p .\tkConfig.py -p .\updateAccount.py  -p framUtil.py -p message.py
if __name__ == '__main__':
    # 是否第一次登录，生成密钥
    check_aes()

    login = LoginForm()
    login.master.mainloop()  # 登录验证

    gui = Gui()
    tkConfig.styles(gui)  # 设置样式
    gui.showAll()  # 展示首页
    gui.master.mainloop()  # 主循环
