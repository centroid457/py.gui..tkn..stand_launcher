from tkinter import Tk

from import_checker import main, python_files_found_in_directory_list, ranked_modules_dict
#print(ranked_modules_dict)      #{}
main(__file__)
#print(ranked_modules_dict)      #{'import_checker': [True, 'py.gui..tkn..stand_launcher', None], }

from gui_tree_import_checker import *

from gui_generate import *
root = Tk()
app = Gui(root=root)
app.mainloop()
