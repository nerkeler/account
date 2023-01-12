import tkConfig
from mainFrame import Gui
from login import LoginForm

def main():
    gui = Gui()
    # 设置样式
    tkConfig.styles(gui)
    # 展示首页
    gui.showAll()
    # 主循环
    gui.master.mainloop()


# 打包命令： pyinstaller -D .\account.py -i .\image\account.ico -w -p .\accountMapper.py -p .\login.py -p .\mainFrame.py -p  .\newAccount.py  -p .\tkConfig.py -p .\updateAccount.py  -p framUtil.py -p message.py
if __name__ == '__main__':
    # login = LoginForm()
    main()
