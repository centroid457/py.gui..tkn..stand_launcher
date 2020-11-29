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
    for file_name in glob("**/*.py*", recursive=True):
        if file_name != os.path.basename(__file__):
            files_found_list.append(file_name)

    print(files_found_list)
    return files_found_list


def find_all_importing_modules(file_list):
    modules_found = set()

    openhook = fileinput.hook_encoded(encoding="utf8", errors=None)
    for line in fileinput.input(files=file_list, mode="r", openhook=openhook):
        #print(f"[descriptor={fileinput.fileno():2}]\tfile=[{fileinput.filename()}]\tline=[{fileinput.filelineno()}]\t[{line}]")
        mask_for_import = r'\s*import\s+(.+)(\s+as\s+.+)?[\t\r\n\f]*'
        mask_for_from_import = r'\s*from\s+(.+)\s+import\s+.*[\t\r\n\f]*'

        match1 = re.fullmatch(mask_for_import, line)
        match2 = re.fullmatch(mask_for_from_import, line)
        #print(match1, match2)

        found_text_group = match1[1] if match1 else match2[1] if match2 else None
        if found_text_group is not None:
            modules_found.update(parse_raw_modules_data(found_text_group))

    print(modules_found)
    return modules_found


def parse_raw_modules_data(raw_modules_data):
    raw_modules_data_wo_spaces = re.sub(r'\s', '', raw_modules_data)
    modules_names_list = raw_modules_data_wo_spaces.split(sep=",")
    return set(modules_names_list)


def detect_incorrect_modules():
    pass


main()
