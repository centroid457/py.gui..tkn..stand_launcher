# print("file frame.py")
import sys
import subprocess
from tkinter import Tk, Frame, Button, Label, BOTH


def main(file_as_path=__file__):
    get_data.main(file_as_path)
    root = Tk()
    app = Gui(root=root, parent=root)
    if close_after_pause_if_ok and get_data.count_found_modules_bad == 0:
        root.after(1000, root.destroy)
    app.mainloop()


# #################################################
# GUI
# #################################################
class Gui(Frame):
    """ main GUI window """
    def __init__(self, root=None, parent=None):
        super().__init__(root)
        self.root = root
        self.parent = parent
        self.gui_root_configure()

        self.create_gui_structure()
        self.window_move_to_center()
        self.fill_table()

    def gui_root_configure(self):
        # ROOT_METHODS
        self.root.title("IMPORT CHECHER")
        self.root.geometry("800x500+100+100")   #("WINXxWINY+ShiftX+ShiftY")
        self.root.resizable(width=True, height=True)	# заблокировать возможность изменения размеров границ! В том числе на весь экран!!!
        #self.root.maxsize(1000, 1000)
        self.root.minsize(300, 300)
        self.root.overrideredirect(False)
        self.root.state('normal')     # normal/zoomed/iconic/withdrawn
        # self.root.iconbitmap(r'ERROR.ico')    =ONLY FILENAME! NO fileobject

        # WM_ATTRIBUTES
        self.root.wm_attributes("-topmost", False)
        self.root.wm_attributes("-disabled", False)
        self.root.wm_attributes("-fullscreen", False)
        self.root.wm_attributes("-transparentcolor", None)

        # WGT_PARAMETERS
        self.root["bg"] = "#005500" if get_data.count_found_modules_bad == 0 else "#FF0000"
        self.root["fg"] = None
        self.root["width"] = None
        self.root["height"] = None
        self.root["bind"] = None
        self.root["relief"] = "raised"  # "flat"/"sunken"/"raised"/"groove"/"ridge"
        self.root["borderwidth"] = 5


    def wgt_parameters_apply(self, wgt, dict_pointer):
        for key in dict_pointer:
            try:
                wgt[key] = dict_pointer[key]
            except:
                pass
                print(f"The object have no attribute [self.root[{key}]]")
        return


    def window_move_to_center(self):
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) / 2
        y = (screen_height - window_height) / 2
        self.root.geometry('+%d+%d' % (x, y))

    # #################################################
    # FRAMES
    # #################################################
    def create_gui_structure(self):
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure([1, 2], weight=0)
        self.parent.rowconfigure(3, weight=1)
        pad_external = 10

        # ======= FRAME-1 (INFO) ====================
        self.frame_info = Frame(self.parent, bg="#101010")
        self.frame_info.grid(row=1, sticky="nsew", padx=pad_external, pady=pad_external)

        lable = Label(self.frame_info, bg="#d0d0d0")
        lable["font"] = ("", 15)
        if get_data.count_found_modules_bad > 0:
            lable["text"] = f"BAD SITUATION:\nYOU NEED INSTALL [{get_data.count_found_modules_bad}] modules"
        else:
            lable["text"] = f"GOOD:\nALL MODULES ARE PRESENT!"
        lable.pack(fill="x", expand=0)

        # ======= FRAME-2 (FILES) ====================
        self.frame_files = Frame(self.parent, bg="#505050", height=30)
        self.frame_files.pack_propagate()  # hear it is necessary
        self.frame_files.grid(row=2, sticky="ew", padx=pad_external, pady=0)

        lable = Label(self.frame_files, bg="#d0d0d0")
        lable["text"] = f"FOUND python [{get_data.count_found_files}]FILES:"
        lable.pack(fill="x", expand=0)

        files_dict = get_data.python_files_found_in_directory_dict
        for file in files_dict:
            lable = Label(self.frame_files, justify="left", anchor="w")
            lable["text"] = file.resolve()
            lable["bg"] = "#99FF99" if files_dict[file].isdisjoint(get_data.modules_found_infiles_bad)\
                else "#FF9999"
            lable.pack(fill="x", expand=0)

        # ======= FRAME-3 (MODULES) ====================
        self.frame_modules = Frame(self.parent, bg="grey")
        self.frame_modules.grid(row=3, sticky="snew", padx=pad_external, pady=pad_external)

        lable = Label(self.frame_modules, bg="#d0d0d0")
        lable["text"] = f"FOUND importing [{get_data.count_found_modules}]modules:"
        lable.pack(fill="x", expand=0)

        # ------- FRAME-3 /1 GOOD -----------------
        self.frame_modules_good = Frame(self.frame_modules, bg="#55FF55")
        self.frame_modules_good.pack(side='left', fill=BOTH, expand=1, padx=1, pady=1)
        self.frame_modules_good.pack_propagate(1)

        # ------- FRAME-3 /2 TRY -----------------
        if get_data.count_found_modules_bad > 0:
            self.frame_modules_try_install = Frame(self.frame_modules, bg="#FF5555")
            self.frame_modules_try_install.pack(side='left', fill=BOTH, expand=1, padx=1, pady=1)
            self.frame_modules_try_install.pack_propagate(1)

            Label(self.frame_modules_try_install,
                  text="if button is green - it will definitly be installed (with internet connection)",
                  bg="#FF5555").pack(fill="x", expand=0)


    def fill_table(self):
        # fill modulenames in gui
        for module in get_data.ranked_modules_dict:
            #[CanImport=True/False, Placement=ShortPathName, InstallNameIfDetected]
            can_import, short_pathname, detected_installname = get_data.ranked_modules_dict[module]
            if can_import:
                Label(self.frame_modules_good, text="%-10s \t[%s]"%(module, short_pathname),
                      fg="black", bg="#55FF55", justify="left", anchor="w", font=('Courier', 9)).pack(fill="x")
            else:
                btn = Button(self.frame_modules_try_install, text=f"pip install [{module}]")
                btn["bg"] = "#55FF55" if detected_installname else None
                btn["command"] = self.start_install_module(module, get_data.ranked_modules_dict[module])
                btn.pack()

    def start_install_module(self, modulename, module_data):
        modulename_cmd = modulename if module_data[2] is None else module_data[2]
        return lambda: (
            subprocess.run(f"py -m pip install {modulename_cmd}"),
            self.program_restart()
        )


    def program_restart(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python_exe = sys.executable
        # If you want to work with correct restart button DO NOT USE ANY PRINT-function befor!!!!
        # else programm will not actually restart (in PyCharm will not start after second Restart)
        os.execl(python_exe, python_exe, *sys.argv)


if __name__ == '__main__':
    close_after_pause_if_ok = False
    import get_data
    main()
else:
    from . import get_data  # main, python_files_found_in_directory_list, ranked_modules_dict
    close_after_pause_if_ok = True
