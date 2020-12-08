import sys
import subprocess
from tkinter import Tk, Frame, Button, Label, BOTH

from import_checker_gui_set import *
from import_checker import *

# #################################################
# GUI
# #################################################
class Gui(Frame):
    """ main GUI window """
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.gui_root_configure()

        self.create_gui_structure()
        self.window_move_to_center()
        self.fill_table()


    def gui_root_configure(self):
        gui_dict_pointer = GUI_ROOT_CONFIGURE_DICT[WM_ATTRIBUTES]
        for k, v in gui_dict_pointer.items():
            eval(f"self.root.{WM_ATTRIBUTES}{k, v}")

        gui_dict_pointer = GUI_ROOT_CONFIGURE_DICT[WGT_PARAMETERS]
        self.wgt_parameters_apply(wgt=self.root, dict_pointer=gui_dict_pointer)

        gui_dict_pointer = GUI_ROOT_CONFIGURE_DICT[ROOT_METHODS]
        for key in gui_dict_pointer:
            if isinstance(gui_dict_pointer[key], (dict)):
                my_func_link = eval(f"self.root.{key}")
                my_func_link(**gui_dict_pointer[key])
            elif isinstance(gui_dict_pointer[key], (tuple)):
                eval(f"self.root.{key}{gui_dict_pointer[key]}")
            else:
                eval(f"self.root.{key}('{gui_dict_pointer[key]}')")

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
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure([1, 2], weight=0)
        self.root.rowconfigure(3, weight=1)
        pad_external = 10

        # ======= FRAME-1 (WINDOW CONTROL) ====================
        self.frame_control = Frame(self.root, bg="#101010")
        self.frame_control.grid(row=1, sticky="nsew", padx=pad_external, pady=pad_external)

        # ======= FRAME-2 (INFO) ====================
        self.frame_info = Frame(self.root, bg="#505050", height=30)
        self.frame_info.pack_propagate()  # hear it is necessary
        self.frame_info.grid(row=2, sticky="ew", padx=pad_external, pady=0)

        lable = Label(self.frame_info, text="if button is green - it will definitly be installed", bg="#d0d0d0")
        lable["text"] = "\n".join(["FOUND FILES:"] + python_files_found_in_directory_list)
        lable.pack(fill="x", expand=0)


        # ======= FRAME-3 (MODULES) ====================
        self.frame_modules = Frame(self.root, bg="grey")
        self.frame_modules.grid(row=3, sticky="snew", padx=pad_external, pady=pad_external)

        # ------- FRAME-3 /1 GOOD -----------------
        self.frame_modules_good = Frame(self.frame_modules, bg="#55FF55", width=200, height=200)
        self.frame_modules_good.pack(side='left', fill=BOTH, expand=1, padx=1, pady=1)
        self.frame_modules_good.pack_propagate(1)

        # ------- FRAME-1 /2 TRY -----------------
        self.frame_modules_try_install = Frame(self.frame_modules, bg="#FF5555")
        self.frame_modules_try_install.pack(side='left', fill=BOTH, expand=1, padx=1, pady=1)
        self.frame_modules_try_install.pack_propagate(1)

        Label(self.frame_modules_try_install, text="if button is green - it will definitly be installed", bg="#FF5555").pack(fill="x", expand=0)


    def fill_table(self):
        # fill modulenames in gui
        for module in ranked_modules_dict:
            #[CanImport=True/False, Placement=ShortPathName, InstallNameIfDetected]
            can_import, short_pathname, detected_installname = ranked_modules_dict[module]
            if can_import:
                Label(self.frame_modules_good, text="%-10s \t[%s]"%(module, short_pathname),
                      fg="black", bg="#55FF55", justify="left", width=20, anchor="w").pack(fill="x", expand=0)
            else:
                btn = Button(self.frame_modules_try_install, text=f"pip install [{module}]")
                btn["bg"] = "#55FF55" if detected_installname else None
                btn["command"] = self.start_install_module(module, ranked_modules_dict[module])
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

