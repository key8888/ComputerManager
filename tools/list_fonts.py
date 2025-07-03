import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont


def list_available_fonts():
    root = tk.Tk()
    root.withdraw()  # ウィンドウを表示しない

    fonts = sorted(tkFont.families())
    for font in fonts:
        print(font)

    root.destroy()
    
list_available_fonts()