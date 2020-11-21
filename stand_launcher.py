from tkinter import Tk, Frame, Button, Label, BOTH
from collections import deque
import sys
import os
from tempfile import NamedTemporaryFile, TemporaryFile
from time import sleep
from subprocess import Popen


# #################################################
# MOUSE MOVING ABILITY
# #################################################
class Grip:
    """ Makes a window dragable by mouse """
    def __init__(self, parent, disable=None, releasecmd=None):
        self.parent = parent
        self.root = parent.winfo_toplevel()

        self.disable = disable
        if type(disable) == 'str':
            self.disable = disable.lower()

        self.releaseCMD = releasecmd

        self.parent.bind('<Button-1>', self.relative_position)
        self.parent.bind('<ButtonRelease-1>', self.drag_unbind)

    def relative_position(self, event):
        cx, cy = self.parent.winfo_pointerxy()
        geo = self.root.geometry().split("+")
        self.oriX, self.oriY = int(geo[1]), int(geo[2])
        self.relX = cx - self.oriX
        self.relY = cy - self.oriY

        self.parent.bind('<Motion>', self.drag_wid)

    def drag_wid(self, event):
        cx, cy = self.parent.winfo_pointerxy()
        d = self.disable
        x = cx - self.relX
        y = cy - self.relY
        if d == 'x':
            x = self.oriX
        elif d == 'y':
            y = self.oriY
        self.root.geometry('+%i+%i' % (x, y))

    def drag_unbind(self, event):
        self.parent.unbind('<Motion>')
        if self.releaseCMD != None:
            self.releaseCMD()


# #################################################
# MAIN GUI
# #################################################
class Gui(Frame):
    """ main GUI window """
    def __init__(self, master=None):
        self.window_state = ('normal', "zoomed")

        super().__init__(master)
        self.master = master
        self.master.title("STAND LAUNCHER")
        self.master["background"] = "black"
        self.create_gui_structure()
        self.create_window_geometry()

    def create_window_geometry(self, moveto00=False):
        if moveto00:   # only move to (0,0)
            self.master.geometry("+0+0")
            return

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 800
        window_height = 200

        x = (screen_width - window_width) / 2
        y = (screen_height - window_height) / 2
        self.master.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

        self.window_set_default_all_functions()

    # #################################################
    # FRAMES
    # #################################################
    def create_gui_structure(self):
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure([1, 2], weight=0)
        self.master.rowconfigure(3, weight=1)

        # ======= FRAME-1 (WINDOW CONTROL) ====================
        self.frame_control = Frame(self.master, bg="#101010")
        self.frame_control.grid(row=1, sticky="nsew", padx=10, pady=10)
        '''Would Be great if it could be specified to only be moved
        when dragging with the Frame above.'''
        grip = Grip(self.frame_control)
        self.create_control_buttons(self.frame_control)

        # ======= FRAME-2 (SETTINGS) ====================
        self.frame_settings = Frame(self.master, bg="#505050", height=30)
        self.frame_settings.pack_propagate(0)   # hear it is necessary
        self.frame_settings.grid(row=2, sticky="ew", padx=10, pady=0)
        self.create_settings_aria(self.frame_settings)

        # ======= FRAME-3 (MAIN WORK SET) ====================
        self.frame_main_work = Frame(self.master, bg="grey")
        self.frame_main_work.grid(row=3, sticky="snew", padx=10, pady=10)

        # ------- FRAME-3 /1 frame LEFT-main menu -----------------
        self.frame_menu_left = Frame(self.frame_main_work, bg="grey", width=200, height=100)
        self.frame_menu_left.pack(side='left', fill=BOTH, expand=0, padx=1, pady=1)
        self.frame_menu_left.pack_propagate(0)
        self.create_work_menu(self.frame_menu_left)

        # ------- FRAME-1 /2 frame CENTER-main work aria -----------------
        self.frame_work_aria = Frame(self.frame_main_work, bg="#ffffff", width=200)
        self.frame_work_aria.pack(side='left', fill=BOTH, expand=1, padx=1, pady=1)
        self.frame_work_aria.pack_propagate(0)
        self.create_work_aria(self.frame_work_aria)

        # ------- FRAME-1 /3 frame RIGHT-error aria -----------------
        self.frame_error_aria = Frame(self.frame_main_work, bg="grey", width=200)
        self.frame_error_aria.pack(side='left', fill=BOTH, expand=0, padx=1, pady=1)
        self.frame_error_aria.pack_propagate(0)
        self.create_work_error_eria(self.frame_error_aria)

    def create_settings_aria(self, master):
        self.create_null_label(master)

    def create_work_menu(self, master):
        self.create_null_label(master)

    def create_work_aria(self, master):
        self.create_null_label(master)

    def create_work_error_eria(self, master):
        self.create_null_label(master)

    def create_null_label(self, master):
        self.label_null = Label(master, text="ПУСТО", fg="white", bg="#505050")
        self.label_null.pack(side="left", fill="x", expand=0)

    # #################################################
    # BUTTONS
    # #################################################
    def get_default_buttons_data(self):
        color_button_normal_set = ["white", "#77FF77"]
        self.button_make_window_default_name="default"
        self.button_data = {
            "button_window_exit": {             # first level it's only id! you can change it any time
                "flag": None,                   # None mean it will always do the same things, flag not used
                "text": "X",                    # text on the button
                "bg": deque(["#FF6666"]),       # second color is for flaged button state, it will rotating
                "command": lambda flag: exit(),
                "side": "left",
                },

            "button_window_fullscreen": {
                "flag": False,
                "text": "^",
                "bg": deque(color_button_normal_set),
                "command": lambda flag: self.window_control_fullscreen(flag=flag),
                "side": "left",
                },

            "button_window_down": {
                "flag": None,
                "text": "_",
                "bg": deque(["white"]),
                "command": lambda flag: self.master.iconify(),
                "side": "left",
                },

            "button_program_reset": {
                "flag": None,
                "text": "reset",
                "bg": deque(["#FF6666"]),
                "command": lambda flag: self.program_reset(),
                "side": "left",
                },

            "button_window_set_default": {
                "flag": None,
                "text": self.button_make_window_default_name,  # DO NOT CHANGE NAME!!! it will couse button not working! see button handler!
                "bg": deque(["white"]),
                "command": lambda widget: self.window_set_default(widget=widget),
                "side": "left",
                },

            "button_window_moveto00": {
                "flag": None,
                "text": "(0.0)",
                "bg": deque(["white"]),
                "command": lambda flag: self.create_window_geometry(moveto00=True),
                "side": "left",
                },

            "button_window_topalways": {
                "flag": False,
                "text": "top",
                "bg": deque(color_button_normal_set),
                "command": lambda flag: self.window_control_top(flag=flag),
                "side": "left",
                },

            "button_window_independent": {
                "flag": False,
                "text": "I",
                "bg": deque(color_button_normal_set),
                "command": lambda flag: self.window_control_independent(flag=flag),
                "side": "left",
                },

            "button_window_settings": {
                "flag": False,
                "text": "Настройки",
                "bg": deque(color_button_normal_set),
                "command": lambda flag: self.frame_settings_open(flag=flag),
                "side": "left",
                },
            }

    def create_control_buttons(self, master):
        self.get_default_buttons_data()
        for i in self.button_data:
            self.create_button(master, i)

    def create_button(self, frame, button_type):
        btn = Button(frame)
        btn["text"] = self.button_data[button_type]["text"]
        btn["width"] = 3 if len(btn["text"]) < 3 else None
        btn["bg"] = self.button_data[button_type]["bg"][0]
        btn.bind("<Button-1>", self.buttons_handle)
        btn.pack(side=self.button_data[button_type]['side'])

    def buttons_handle(self, event):
        for button_id in self.button_data:
            if self.button_data[button_id]["text"] == event.widget["text"]:
                if self.button_data[button_id]["text"] == self.button_make_window_default_name:
                    self.button_data[button_id]["command"](widget=event.widget)
                    return

                self.button_data[button_id]["bg"].rotate()
                flag_old = self.button_data[button_id]["flag"]
                flag_new = None if flag_old == None else not (flag_old)
                self.button_data[button_id]["flag"] = flag_new
                event.widget["bg"] = self.button_data[button_id]["bg"][0]
                self.button_data[button_id]["command"](flag=flag_new)
                return

    # BUTTON FUNCTIONS
    def window_set_default_all_functions(self):
        self.window_control_fullscreen(flag=False)
        self.window_control_top(flag=False)
        self.window_control_independent(flag=False)
        self.frame_settings_open(flag=False)
        self.get_default_buttons_data()

    def window_control_fullscreen(self, flag=False):
        self.master.state(self.window_state[int(flag)])
        if not flag:
            self.master.wm_attributes('-fullscreen', flag)

    def window_control_top(self, flag=False):
        self.master.wm_attributes("-topmost", flag)

    def window_set_default(self, widget):
        self.get_default_buttons_data()
        remaining_buttons_to_reset = self.button_data.copy()

        parent_widget_name = widget.winfo_parent()      # .!frame
        parent_widget_obj = widget._nametowidget(parent_widget_name)
        button_obj_list = parent_widget_obj.pack_slaves()

        for widget_obj in button_obj_list:
            for button_id in remaining_buttons_to_reset:
                if remaining_buttons_to_reset[button_id]["text"] == widget_obj["text"]:
                    poped_button = remaining_buttons_to_reset.pop(button_id)
                    widget_obj["bg"] = poped_button["bg"][0]
                    break

        self.window_set_default_all_functions()
        self.create_window_geometry()

    def window_control_independent(self, flag=False):
        """make window independent from OS explorer"""
        self.master.wm_overrideredirect(flag)

    def frame_settings_open(self, flag=False):
        if flag:
            self.frame_settings.grid()
        else:
            self.frame_settings.grid_remove()

    def program_reset(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python_exe = sys.executable
        os.execl(python_exe, python_exe, *sys.argv)
        #sleep(3)

def main():
    #check_program_instances()
    root = Tk()
    app = Gui(master=root)
    app.mainloop()

def check_program_instances():
    prefix = "started_"
    suffix = "_instance.check"
    dir_current = os.path.dirname(__file__)
    temp_file = TemporaryFile(suffix=suffix, prefix=prefix, dir=dir_current)
    print(temp_file.name)  # C:\!CENTROID\ProjectsPYTHON\test2\started_65hqjser_instance.check
    #sleep(3)

if __name__ == '__main__':
    main()
