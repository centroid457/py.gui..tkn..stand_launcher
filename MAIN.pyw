# ##########################################################
# PLACE THIS BLOCK AT FIRST LINE! AND PLACE YOUR ALL IMPORTS AFTER!!!
import sys
sys.path.append("C:\\!CENTROID\\ProjectsPYTHON\\!MODULES\\")
import import_checker
import_checker.frame.start_gui(__file__)
# ##########################################################

# import test123
from tkinter import Tk, Frame, Button, Label
from tkinter import ttk
import frame_root_control


def main():
    root = Tk()
    root.geometry("800x300")

    root.columnconfigure(0, weight=1)
    root.rowconfigure([0, ], weight=0)
    root.rowconfigure([1, ], weight=1)
    pad_external = 2

    # ======= FRAME-0 (WINDOW CONTROL) ====================
    frame_control = Frame(root, bg="#101010")
    frame_control.grid(row=0, sticky="ew", padx=pad_external, pady=pad_external)

    frame_root_control.Gui(frame_control)

    # ======= FRAME-1 (DATA) ====================
    frame_nb = ttk.Notebook(root)
    frame_nb.grid(row=1, sticky="snew", padx=pad_external, pady=0)

    tab_1 = Frame(frame_nb, bg="#00FF00", height=100)
    frame_nb.add(tab_1, text="tab1")

    tab_2 = Frame(frame_nb, bg="#0000FF", height=100)
    frame_nb.add(tab_2, text="Import Checker")

    tab_2_data = import_checker.frame.Gui(parent=tab_2, path_link=__file__)
    tab_2_data.grid(sticky="snew")

    root.mainloop()


if __name__ == '__main__':
    main()
