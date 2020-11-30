"""
it will find import in all files only in current directory!
Check modules which will import in project.
find not installed.
offer try to install.
"""

import re
import os
import pkgutil
import fileinput
from glob import glob


modules_must_install = {
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
    modules_found_built_in = []
    modules_found_installed = []
    modules_found_not_installed = []
    modules_found_not_recognized = []

    python_files_found_in_directory_list = find_all_python_files()
    modules_found_in_files_set = find_all_importing_modules(python_files_found_in_directory_list)
    rank_modules_result = rank_modules(modules_found_in_files_set)


def find_all_python_files(path=None):
    # by default find all modules in current directory with all subdirectories
    files_found_list = []
    for file_name in glob("**/*.py*", recursive=True):
        if file_name != os.path.basename(__file__):
            files_found_list.append(file_name)

    print(files_found_list)
    return files_found_list


def find_all_importing_modules(file_list):
    # 1. find all import strings in all files
    # 2. parse all module names in them
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
            modules_found.update(_parse_raw_modules_data(found_text_group))

    print(modules_found)
    return modules_found


def _parse_raw_modules_data(raw_modules_data):
    raw_modules_data_wo_spaces = re.sub(r'\s', '', raw_modules_data)
    modules_names_list = raw_modules_data_wo_spaces.split(sep=",")
    return set(modules_names_list)

def rank_modules(modules_in_files_set):
    modules_in_files_ranked_dict = {}
    modules_in_system_dict = _get_system_modules()


    return
    for module in modules_in_files_set:
        print(module)
        modules_in_files_ranked_dict.update({module:modules_in_system_dict[module]})
        print(modules_in_files_ranked_dict)
    print(modules_in_files_ranked_dict)
    return modules_in_files_ranked_dict


def _get_system_modules():
    modules_in_system = {}

    for module_in_system in pkgutil.iter_modules():
        #print(module_in_system.name)
        my_string = str(module_in_system.module_finder)
        # print(my_string)
        mask = r".*[\\/]+([^\\/']+)['\)]+$"
        match = re.fullmatch(mask, my_string)
        modules_in_system.update({module_in_system.name:match[1]})

    print(modules_in_system)
    return modules_in_system


main()
