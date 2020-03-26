import os
import platform
import tkinter
from typing import List


class DragDropListbox(tkinter.Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """

    def __init__(self, master, **kw):
        kw["selectmode"] = tkinter.SINGLE
        tkinter.Listbox.__init__(self, master, kw)
        self.bind("<Button-1>", self.setCurrent)
        self.bind("<B1-Motion>", self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i + 1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i - 1, x)
            self.curIndex = i

    def get_list_items(self):
        return super().get(0, tkinter.END)


def user_set_lro(teams: List[str]):
    window = tkinter.Tk()
    window.title("DragNDrop Priority")
    d = DragDropListbox(window)
    d.pack()
    for team in teams:
        d.insert(tkinter.END, team)

    ret_list = None

    def on_closing():
        nonlocal ret_list
        ret_list = list(d.get_list_items())
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)
    if platform.system() == "Darwin":  # How Mac OS X is identified by Python
        os.system("""/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' """)
    window.after(1, lambda: window.focus_force())
    window.mainloop()
    return ret_list
