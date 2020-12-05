"""
HOW TO USE:
1. add in .gitignore line "__pycache__"
2. add this script to your project directory
3. add lines in your main script in place before first import line:
*********************
import import_checker
import_checker.main(file_for_path=__file__)
*********************
WHAT IT WILL DO
Find all import lines in all files in the directory with recursion!
Lines only with SPACE symbols before specific code words.
Check modules which will import in project.
Find not installed.
Offer try to install.
---------------------
WHY DON'T USE MODULEFINDER???
Because it work incorrect! can't find TIME and SYS modules!
---------------------
TEST LINE
import TEST_LINE1
#import TEST_LINE2
"""

import re
import os
import sys
import pkgutil
import fileinput
import subprocess
from glob import glob
from tkinter import Tk, Frame, Button, Label, BOTH


modules_can_install = {
    # "IMPORT NAME IN PROJECT": "PIP INSTALL NAME"
    # different names
    "wx": "wxPython",
    "PIL": "pillow",

    # similare names
    "TEST_LINE1": "TEST_LINE1",
    "plotly": "plotly",
    "pandas": "pandas",
    "pygame": "pygame",
    "psutil": "psutil",
    "pystray": "pystray",
    "requests": "requests",
    "tabulate": "tabulate",
    "openpyxl": "openpyxl",
    "playsound": "playsound",
    "matplotlib": "matplotlib",
    "pyscreenshot": "pyscreenshot",
}

MARK_MODULE_BAD = "###BAD###"
modules_found_infiles = set()
modules_in_system_dict = {}


def main(file_for_path=__file__):
    global python_files_found_in_directory_list
    path_find_wo_slash = os.path.dirname(file_for_path)
    python_files_found_in_directory_list = find_all_python_files(path=path_find_wo_slash)
    find_all_importing_modules(python_files_found_in_directory_list)
    ranked_modules_dict = rank_modules(modules_found_infiles)

    root = Tk()
    app = Gui(root=root, modules_data=ranked_modules_dict)
    app.mainloop()


def find_all_python_files(path):
    # by default find all modules in current directory with all subdirectories
    files_found_list = []
    for file_name in glob(path+"/**/*.py*", recursive=True):
        if file_name != os.path.basename(__file__) and os.path.splitext(file_name)[1] in (".py", ".pyw"):
            files_found_list.append(file_name)

    # print(files_found_list)
    return files_found_list


def find_all_importing_modules(file_list):
    # 1. find all import strings in all files
    # 2. parse all module names in them

    openhook = fileinput.hook_encoded(encoding="utf8", errors=None)
    for line in fileinput.input(files=file_list, mode="r", openhook=openhook):
        #print(f"[descriptor={fileinput.fileno():2}]\tfile=[{fileinput.filename()}]\tline=[{fileinput.filelineno()}]\t[{line}]")
        modules_found_infiles.update(_find_modulenames_set(line))

    #print(modules_found_infiles)
    return


def _find_modulenames_set(line):
    # find lines with import statement
    # return modulenames
    line_wo_comments = line.split(sep="#")[0]
    modules_found_inline = set()

    mask_import_as = r'\s*import\s+(.+?)(\s+as\s+.+)?[\t\r\n\f]*'
    mask_from_import = r'\s*from\s+(.+)\s+import\s+.*[\t\r\n\f]*'

    match1 = re.fullmatch(mask_import_as, line_wo_comments)
    match2 = re.fullmatch(mask_from_import, line_wo_comments)

    found_modulenames_group = match1[1] if match1 else match2[1] if match2 else None
    if found_modulenames_group is not None:
        modules_found_inline = _split_module_names_set(found_modulenames_group)

    return modules_found_inline

def _split_module_names_set(raw_modulenames_data):
    raw_modules_data_wo_spaces = re.sub(r'\s', '', raw_modulenames_data)
    modules_names_list = raw_modules_data_wo_spaces.split(sep=",")
    return set(modules_names_list)

assert _split_module_names_set("m1,m2 ,m3,    m4,\tm5") == set([f"m{i}" for i in range(1, 6)])
assert _find_modulenames_set("import\tm1") == {"m1"}
assert _find_modulenames_set("#import\tm1") == set()
assert _find_modulenames_set(" import\t m1,m2") == {"m1", "m2"}
assert _find_modulenames_set(" import\t m1 as m2") == {"m1"}
assert _find_modulenames_set(" from m1 import m2 as m3") == {"m1"}
assert _find_modulenames_set("#from m1 import m2 as m3") == set()
assert _find_modulenames_set("import m1 #comment import m2") == {"m1"}


def rank_modules(modules_in_files_set):
    modules_in_files_ranked_dict = {}
    modules_in_system_dict = _get_system_modules()
    for module in modules_in_files_set:
        try:
            exec(f'import {module}')
            modules_in_files_ranked_dict.update({module:modules_in_system_dict[module] if module in modules_in_system_dict else "+++GOOD+++"})
        except:
            modules_in_files_ranked_dict.update({module: MARK_MODULE_BAD})

    #print(modules_in_files_ranked_dict)
    return modules_in_files_ranked_dict


def _get_system_modules():
    # all modules detecting in system! in all available paths. (Build-in, Installed, located in current directory)
    for module_in_system in pkgutil.iter_modules():
        #print(module_in_system.name)
        my_string = str(module_in_system.module_finder)
        # print(my_string)
        mask = r".*[\\/]+([^\\/']+)['\)]+$"
        match = re.fullmatch(mask, my_string)
        modules_in_system_dict.update({module_in_system.name:match[1]})

    #print(modules_in_system_dict)
    return modules_in_system_dict

# #################################################
# GUI
# #################################################
class Gui(Frame):
    """ main GUI window """
    def __init__(self, root=None, modules_data=None):
        super().__init__(root)
        self.root = root
        self.modules_data = modules_data
        self.gui_general_configure()
        self.create_gui_structure()
        self.create_gui_geometry()
        self.fill_table()

    def gui_general_configure(self):
        self.root.title("IMPORT CHECHER")
        self.root["bg"] = "black"

    def create_gui_geometry(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 800
        window_height = 200
        x = (screen_width - window_width) / 2
        y = (screen_height - window_height) / 2
        self.root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

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
        for module in self.modules_data:
            self.module_can_install_check = module in modules_can_install
            if self.modules_data[module] != MARK_MODULE_BAD:
                Label(self.frame_modules_good, text=module, fg="black", bg="#55FF55").pack(fill="x", expand=0)
            else:
                btn = Button(self.frame_modules_try_install, text=f"pip install [{module}]")
                btn["bg"] = "#55FF55" if self.module_can_install_check else None
                btn["command"] = self.start_install_module(module)
                btn.pack()

    def start_install_module(self, module_name):
        module_name_cmd = modules_can_install[module_name] if self.module_can_install_check else module_name
        return lambda: (
            subprocess.run(f"py -m pip install {module_name_cmd}"),
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
    main()
