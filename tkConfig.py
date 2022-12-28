from tkinter.ttk import *


def query(db, gui):
    row_count = 1
    for item in db.query_all():
        account = list(item)
        account[3] = "************"
        if row_count % 2 == 1:
            gui.insert(account[0], account[1:], '')
        else:
            gui.insert(account[0], account[1:], ("evenColor"))
        row_count += 1


def styles(gui):
    s = Style()
    s.configure('Treeview', rowheight=30)
    s.configure('Entry', height=30)
    s.configure('Treeview', font=('Microsoft YaHei', 10))
    gui.dropDown.current(0)
