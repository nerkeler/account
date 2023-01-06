import tkConfig
from mainFrame import Gui


def main():
    gui = Gui()
    # 设置样式
    tkConfig.styles(gui)
    # 展示首页
    gui.showAll()
    # 主循环
    gui.master.mainloop()


# 打包命令： pyinstaller -D .\main.py -i .\image\account.ico -w -p .\accountMapper.py -p .\login.py -p .\mainFrame.py -p
# .\newAccount.py  -p .\tkConfig.py -p .\updateAccount.py


if __name__ == '__main__':
    main()
