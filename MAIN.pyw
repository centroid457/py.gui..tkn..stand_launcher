# ##########################################################
# PLACE THIS BLOCK AT FIRST LINE! AND PLACE YOUR ALL IMPORTS AFTER!!!
import sys
sys.path.append("C:\\!CENTROID\\ProjectsPYTHON\\!MODULES\\")
import import_checker
import_checker.frame.start_gui(__file__)
# ##########################################################

#import test123
from tkinter import Tk, Frame, Button, Label
import frame_root_control


def main():
    root = Tk()

    root.columnconfigure(0, weight=1)
    root.rowconfigure([0, ], weight=0)
    root.rowconfigure([1, ], weight=1)
    pad_external = 3

    # ======= FRAME-0 (WINDOW CONTROL) ====================
    frame_control = Frame(root, bg="#101010")
    # frame_control.pack_propagate(0)
    frame_control.grid(row=0, sticky="ew", padx=pad_external, pady=pad_external)

    frame_root_control.Gui(frame_control)

    # ======= FRAME-1 (SETTINGS) ====================
    frame_1 = Frame(root, bg="#505050", height=30)
    # frame_1.pack_propagate(1)
    frame_1.grid(row=1, sticky="snew", padx=pad_external, pady=0)

    root.mainloop()


if __name__ == '__main__':
    main()
