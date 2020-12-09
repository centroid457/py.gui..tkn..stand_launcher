from tkinter import Tk

from import_checker import main, python_files_found_in_directory_list, ranked_modules_dict
#print(ranked_modules_dict)      #{}
main(__file__)
#print(ranked_modules_dict)      #{'import_checker': [True, 'py.gui..tkn..stand_launcher', None], }

from import_checker_gui_set import *

from import_checker_gui import *
root = Tk()
app = Gui(root=root)
app.mainloop()
