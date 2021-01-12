# DO NOT USE ANY PRINT() FUNCTIONS! ONLY for debug purpose!! else it will brake program_restart()!

# #################################################
# LIBS
# #################################################
import json
import os
import sys
import pathlib

from glob import glob
from time import sleep
from tkinter import Tk, Frame, Button, Label
from tempfile import NamedTemporaryFile
from threading import Thread

# NEED TO INSTALL
from PIL import Image, ImageDraw, ImageFont     # pip3 install pillow
from pystray import Icon, Menu, MenuItem        # pip3 install pystray

# #################################################
# SETTINGS = dirnames / filenames
# #################################################
dirname_current = pathlib.Path.cwd()
dirname_settings = dirname_current / "settings"
dirname_settings.mkdir(exist_ok=True)
filename_btns_settings = dirname_current / "settings" / "settings_root_control_btns.json"

filename_program_image = dirname_settings / "program_icon.ico"
filename_program_save_state = dirname_settings / ".program_save_state.pickle"

program_instance_prefix = ".started_"
program_instance_suffix = "_instance.check"


# #################################################
# MOUSE MOVING ABILITY
# #################################################
class Make_gui_draggable:
    """ Makes a window draggable by mouse """
    def __init__(self, parent):
        self.parent = parent
        self.root = parent.winfo_toplevel()

        self.parent.bind('<Button-1>', self.start)
        self.parent.bind('<ButtonRelease-1>', self.stop)

    def start(self, event):
        self.pointer_start_x, self.pointer_start_y = self.parent.winfo_pointerxy()
        root_start_xy = self.root.geometry().split("+")
        self.root_start_x, self.root_start_y = int(root_start_xy[1]), int(root_start_xy[2])

        wgt_under_pointer = self.root.winfo_containing(self.pointer_start_x, self.pointer_start_y)
        wgt_name = str(wgt_under_pointer)
        wgt_names_dont_move_list = ["scrollbar", ]
        for wgt in wgt_names_dont_move_list:
            if wgt in wgt_name:
                return

        if "button" in wgt_name and event.widget._nametowidget(wgt_name)["state"] != "disabled":
            return

        self.parent.bind('<Motion>', self.drag)

    def drag(self, event):
        pointer_next_x, pointer_next_y = self.parent.winfo_pointerxy()
        next_x = pointer_next_x - self.pointer_start_x + self.root_start_x
        next_y = pointer_next_y - self.pointer_start_y + self.root_start_y
        self.root.geometry('+%i+%i' % (next_x, next_y))

    def stop(self, event):
        self.parent.unbind('<Motion>')


# #################################################
# MAIN GUI
# #################################################
class Gui(Frame):
    """ main GUI window """
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.root = self.winfo_toplevel()

        self.check_program_instances()
        self.create_icon()

        Thread(target=self.tray_icon_start, args=(), daemon=True).start()

        self.create_gui_structure()

        self.gui_root_configure()
        self.window_move_to_center()

    def __del__(self):
        print("execute destructor")
        self.program_save_state()

    def check_program_instances(self):
        mask = f"{str(dirname_settings)}" + '\\'\
                    f"{program_instance_prefix}"\
                    f"*{program_instance_suffix}"
        if len(glob(mask)):
            raise Exception("Program already have earlier started instance. Can't start new one!")
        else:
            self.create_program_instance_filemark()

    def create_program_instance_filemark(self):
        self.temporary_file = NamedTemporaryFile(
            suffix=program_instance_suffix,
            prefix=program_instance_prefix,
            dir=dirname_settings)

    def gui_root_configure(self):
        if self.root == self.parent:      # if it is independent window (without insertion in outside project)
            self.root.title("STAND LAUNCHER")
            self.root["bg"] = "black"
            self.root.geometry("800x60")

        # IF YOU WANT TO DISABLE - CHANGE TO NONE or COMMENT OUT
        # ROOT_METHODS = many of them can named with WM! geometry=WM_geometry
        # self.root.title("STAND LAUNCHER")
        self.root.iconbitmap(filename_program_image)   # ONLY FILENAME! NO fileobject
        self.root.protocol('WM_DELETE_WINDOW', self.program_exit)  # intersept gui exit()

        # self.root.geometry("800x500+100+100")           #("WINXxWINY+ShiftX+ShiftY")
        self.root.geometry("800x600")                 #("WINXxWINY")
        # self.root.geometry("+100+100")                #("+ShiftX+ShiftY")
        # self.root.resizable(width=True, height=True)    # block resizable! even if fullscreen!!!
        # self.root.maxsize(1000, 1000)
        # self.root.minsize(800, 300)

        # self.root.overrideredirect(False)   # borderless window, without standard OS header and boarders
        # self.root.state('zoomed')   # normal/zoomed/iconic/withdrawn
        # self.root.iconify()       # ICONIFY/deiconify = hide down window, minimize
        # self.root.withdraw()      # WITHDRAW/deiconify = hide out window, don't show anywhere
        # self.root.deiconify()     # restore window

        # WM_ATTRIBUTES = root.wm_attributes / root.attributes
        # self.root.wm_attributes("-topmost", False)
        # self.root.wm_attributes("-disabled", False)     # disable whole gui
        # self.root.wm_attributes("-fullscreen", False)
        # self.root.wm_attributes("-transparentcolor", None)

        # WGT_PARAMETERS = ROOT.CONFIG(bg="red") / ROOT["bg"]="red"
        # self.root["bg"] = "black"
        # self.root["fg"] = None
        # self.root["width"] = None
        # self.root["height"] = None
        # self.root["bind"] = None
        # self.root["relief"] = "raised"  # "flat"/"sunken"/"raised"/"groove"/"ridge"
        # self.root["borderwidth"] = 5
        # self.root["cursor"] = None   # 'watch'=the best / "xterm" / "arrow"=standard

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
    # TRAY
    # #################################################
    def create_icon(self):
        if os.path.exists(filename_program_image):
            return
        box = 32
        size_ico = (box, box)
        band_gradient = Image.linear_gradient("L")
        R = band_gradient.copy()
        G = R.copy().rotate(90)
        B = R.copy().rotate(-90)
        image_obj = Image.merge("RGB", (R, G, B))
        font = ImageFont.truetype("arial.ttf", 190)
        drawing = ImageDraw.Draw(image_obj)
        drawing.text((9, 20), "ST", font=font, fill=(0, 0, 0))
        image_obj.thumbnail(size_ico)
        image_obj.save(filename_program_image)
        return

    def tray_icon_start(self):
        tray_icon_obj = Icon('tray name')
        tray_icon_obj.icon = Image.open(filename_program_image)
        menu = Menu(
            MenuItem(text='РАСКРЫТЬ', action=self.tray_action_show_gui, default=True),
            MenuItem(text='ВЫХОД', action=self.tray_action_exit)
        )
        tray_icon_obj.menu = menu
        tray_icon_obj.run()

    def tray_action_show_gui(self):
        self.root.deiconify()

    def tray_action_exit(self):
        self.program_exit()

    # #################################################
    # FRAMES
    # #################################################
    def create_gui_structure(self):
        Make_gui_draggable(self.root)

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure([0, 1, ], weight=0)
        pad_external = 5

        # ======= FRAME-0 (WINDOW CONTROL) ====================
        self.frame_control = Frame(self.parent, bg="#101010")
        self.frame_control.grid(row=0, sticky="nsew", padx=pad_external, pady=pad_external)

        # ======= FRAME-1 (SETTINGS) ====================
        self.frame_settings = Frame(self.parent, bg="#505050", height=30)
        self.frame_settings.grid(row=1, sticky="ew", padx=pad_external, pady=0)

        self.fill_all_frames()

    def fill_all_frames(self):
        # PLACE IT ONLY AFTER ALL FRAMES INITIATION!!!
        self.create_gui_control_buttons(self.frame_control)
        self.create_settings_aria(self.frame_settings)

    def create_settings_aria(self, root):
        self.create_null_label(root)

    def create_null_label(self, root):
        self.label_null = Label(root, text="ПУСТО", fg="white", bg="#505050")
        self.label_null.pack(side="left", fill="x", expand=0)

    # #################################################
    # BUTTONS
    # #################################################
    def create_gui_control_buttons(self, parent):
        self.btn_window_blank = ButtonMod(parent=parent, flag_default=None, bg_default=None, func=None)
        self.btn_window_blank["text"] = chr(9995)
        self.btn_window_blank["state"] = "disabled"
        self.btn_window_blank.pack(side="left")

        self.btn_window_switch_to_default = ButtonMod(parent=parent, flag_default=None, bg_default=None, func=self.window_set_default)
        self.btn_window_switch_to_default["text"] = "default"
        self.btn_window_switch_to_default.pack(side="left")

        self.btn_window_short = ButtonMod(parent=parent, flag_default=None, bg_default=None, func=self.window_control_short)
        self.btn_window_short["text"] = chr(9624)
        self.btn_window_short.pack(side="left")

        self.btn_window_exit = ButtonMod(parent=parent, flag_default=None, bg_default="#FF6666", func=self.program_exit)
        self.btn_window_exit["text"] = chr(9587)
        self.btn_window_exit.pack(side="left")

        self.btn_window_fullscreen = ButtonMod(parent=parent, flag_default=False, bg_default=None, func=self.window_control_fullscreen)
        self.btn_window_fullscreen["text"] = chr(9744)
        self.btn_window_fullscreen.pack(side="left")

        self.btn_window_minimize = ButtonMod(parent=parent, flag_default=None, bg_default=None, func=self.window_control_minimize)
        self.btn_window_minimize["text"] = "_"
        self.btn_window_minimize.pack(side="left")

        self.btn_program_restart = ButtonMod(parent=parent, flag_default=None, bg_default="#FF6666", func=self.program_restart)
        self.btn_program_restart["text"] = "restart"
        self.btn_program_restart.pack(side="left")

        self.btn_window_moveto00 = ButtonMod(parent=parent, flag_default=None, bg_default=None, func=self.window_control_move_to_00)
        self.btn_window_moveto00["text"] = chr(8689)
        self.btn_window_moveto00.pack(side="left")

        self.btn_window_topalways = ButtonMod(parent=parent, flag_default=True, bg_default=None, func=self.window_control_topalways)
        self.btn_window_topalways["text"] = "top"
        self.btn_window_topalways.pack(side="left")

        self.btn_window_independent = ButtonMod(parent=parent, flag_default=True, bg_default=None, func=self.window_control_independent)
        self.btn_window_independent["text"] = chr(10043)
        self.btn_window_independent.pack(side="left")

        self.btn_window_settings = ButtonMod(parent=parent, flag_default=False, bg_default=None, func=self.frame_settings_open)
        self.btn_window_settings["text"] = "Settings"
        self.btn_window_settings.pack(side="left")

        self.btns_apply_saved_state()

    def btns_apply_saved_state(self):
        if not filename_btns_settings.exists():
            return

        with open(filename_btns_settings, "r") as file_obj:
            saved_state_dict = json.load(file_obj)

        for btn in ButtonMod.buttonmod_flagged_list:
            btn_last_name = str(btn).rsplit(".", maxsplit=1)[1]
            if btn_last_name in saved_state_dict:
                btn.switch_set_flag(flag=saved_state_dict[btn_last_name][0])
        return

    def btns_save_state(self):
        saved_state_dict = {}
        for btn in ButtonMod.buttonmod_flagged_list:
            # print(btn.winfo_name(), btn.flag_default, btn["text"])
            saved_state_dict[btn.winfo_name()] = [btn.flag_active, btn["text"]]
        # print(saved_state_dict)
        with open(filename_btns_settings, "w") as file_obj:
            json.dump(saved_state_dict, file_obj, ensure_ascii=True, indent=True)
        return

    def window_set_default(self):
        for btn_control in ButtonMod.buttonmod_flagged_list:
            btn_control.switch_default()
        self.gui_root_configure()
        self.window_move_to_center()

    def window_control_short(self, flag=True):
        if flag:
            self.btn_window_topalways.switch_set_flag(flag=True)
            self.btn_window_fullscreen.switch_set_flag(flag=False)
            self.btn_window_independent.switch_set_flag(flag=True)
            window_width = 130       # it does not matter if less then about 120!!!
            window_height = 40
            self.root.geometry('%dx%d+%d+%d' % (window_width, window_height, 0, 0))

    def window_control_fullscreen(self, flag=False):
        window_state = ('normal', "zoomed")
        self.root.state(window_state[int(flag)])
        if not flag:
            self.root.wm_attributes('-fullscreen', flag)

    def window_control_minimize(self):
        if not self.btn_window_independent.flag_active:
            self.root.iconify()
        else:
            self.root.withdraw()

    def window_control_move_to_00(self):
        self.root.geometry("+0+0")

    def window_control_topalways(self, flag=False):
        self.root.wm_attributes("-topmost", flag)

    def window_control_independent(self, flag=False):
        """make window independent from OS explorer"""
        self.root.wm_overrideredirect(flag)

    def frame_settings_open(self, flag=False):
        if flag:
            self.frame_settings.grid()
        else:
            self.frame_settings.grid_remove()

    # #################################################
    # PROGRAM CONTROL
    # #################################################
    def program_restart(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        self.program_save_state()
        python_exe = sys.executable
        # If you want to work with correct restart button DO NOT USE ANY PRINT-function before!!!!
        # else program will not actually restart (in PyCharm will not start after second Restart)
        os.execl(python_exe, python_exe, *sys.argv)

    def program_exit(self):
        self.program_save_state()
        print("exit")
        self.root.destroy()

    def program_save_state(self, data_to_save=None):
        pass
        self.btns_save_state()


class ButtonMod(Button):
    color_off_on = ["white", "#77FF77"]
    buttonmod_flagged_count = 0
    buttonmod_flagged_list = []

    def __init__(self, parent=None, flag_default=None, bg_default=None, func=None):
        super().__init__(parent)
        self.parent = parent

        self.is_flagged = False if flag_default is None else True
        self.flag_default = flag_default
        self.flag_active = flag_default

        self.bg_set = ButtonMod.color_off_on if bg_default is None else [bg_default, ButtonMod.color_off_on[1]]
        self["bg"] = self.bg_set[0]

        self.func = func if func is not None else lambda flag=False: None
        self["command"] = self.switch

        if self.is_flagged:
            ButtonMod.buttonmod_flagged_count += 1
            ButtonMod.buttonmod_flagged_list += [self]
            self.switch_default()

    def switch(self):
        self.switch_set_flag(not self.flag_active)

    def switch_default(self):
        self.switch_set_flag(self.flag_default)

    def switch_set_flag(self, flag):
        if self.is_flagged:
            self.flag_active = flag
            self["bg"] = self.bg_set[int(flag)]
            self.func(flag)
        else:
            self.func()


def main():
    root = Tk()
    app = Gui(parent=root)
    app.mainloop()


if __name__ == '__main__':
    main()
