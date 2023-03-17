from tkinter.ttk import *


def styles(gui):
    s = Style()
    s.configure('Treeview', rowheight=30)
    s.configure('Entry', height=30)
    s.configure('Treeview', font=('Microsoft YaHei', 10))
    gui.dropDown.current(0)
