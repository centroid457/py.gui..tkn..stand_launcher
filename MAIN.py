from tkinter import Tk

from import_checker import main, python_files_found_in_directory_list, ranked_modules_dict
print(ranked_modules_dict)      #{}
main()
print(ranked_modules_dict)      #{'PIL': 'site-packages', 'time': '+++GOOD+++', 'pkgutil': 'lib',///}

from gui_tree_import_checker import *

from gui_generate import *
root = Tk()
app = Gui(root=root)
app.mainloop()
