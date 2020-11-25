"""
it will find import in all files only in current directory!
Check modules which will import in project.
find not installed.
offer try to install.
"""

import re
import os
import fileinput
from glob import glob

modules_need_to_install = {
    # "IMPORT NAME IN PROJECT", "PIP INSTALL NAME")
    # different names
    "PIL": "pillow",
    "wx": "wxPython",

    # similare names
    "pystray": "pystray",
    "psutil": "psutil",
    "tabulate": "tabulate",
    "openpyxl": "openpyxl",
    "pandas": "pandas",
    "pyscreenshot": "pyscreenshot",
    "playsound": "playsound",
    "matplotlib": "matplotlib",
    "plotly": "plotly",
    "pygame": "pygame",
    "requests": "requests",
}


def main():
    python_files_found_in_directory = []

    modules_found_all = []
    modules_found_built_in = []
    modules_found_installed = []
    modules_found_not_installed = []
    modules_found_not_recognized = []

    python_files_found_in_directory = find_all_python_files()
    modules_found_all = find_all_importing_modules(python_files_found_in_directory)


def find_all_python_files(path=None):
    files_found_list = []
    for file_name in glob("*.py*"):
        if file_name != os.path.basename(__file__):
            files_found_list.append(file_name)

    print(files_found_list)
    return files_found_list

def find_all_importing_modules(file_list):
    print(file_list)
    modules_found = set()
    try:
        for line in fileinput.input(files=file_list, mode="r"):
            print(f"[descriptor={fileinput.fileno():2}]\tfile=[{fileinput.filename()}]\tline=[{fileinput.filelineno()}]\t[{line}]")
            mask_for_import = r'\s*import\s+(.+)(\s+as\s+.+)?[\t\r\n\f]*'
            mask_for_from_import = r'\s*from\s+(.+)\s+import\s+.*[\t\r\n\f]*'

            match1 = re.fullmatch(mask_for_import, line)
            match2 = re.fullmatch(mask_for_from_import, line)
            if match1: modules_found.add(match1[1])
            if match2: modules_found.add(match2[1])
            print(match1, match2)
    except:
        pass

    print(modules_found)
    return modules_found

def detect_incorrect_modules():
    pass


main()
