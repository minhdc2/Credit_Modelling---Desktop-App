from tkinter import *
import gui.menu as gm
import gui.main_page as gmp

if __name__ == '__main__':
    root = Tk()
    root.geometry("1200x550")
    root.config(bg='white')
    gm.MenuTab(root)
    gmp.MainPage(root)
    root.mainloop()