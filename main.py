from mainFrame import Gui
from accountMapper import Db
import tkConfig

# 初始化数据库对象和GUI对象
db = Db()
gui = Gui()


# 设置样式
tkConfig.styles(gui)
tkConfig.query(db, gui)

if __name__ == '__main__':

    gui.master.mainloop()

