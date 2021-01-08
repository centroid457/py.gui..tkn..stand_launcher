# DO NOT USE ANY PRINT() FUNCTIONS! ONLY for debug purpose!! else it will brake program_restart()!

# #################################################
# LIBS
# #################################################
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

filename_program_image = dirname_settings / "program_icon.ico"
filename_program_save_state = dirname_settings / ".program_save_state.pickle"

program_instance_prefix = ".started_"
program_instance_suffix = "_instance.check"


# #################################################
# MOUSE MOVING ABILITY
# #################################################
class Make_gui_draggable:
    """ Makes a window draggable by mouse """
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
        if self.releaseCMD is not None:
            self.releaseCMD()


# #################################################
# MAIN GUI
# #################################################
class Gui(Frame):
    """ main GUI window """
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.root = self.parent.winfo_toplevel()
        Make_gui_draggable(self.root)

        self.check_program_instances()
        self.create_icon()

        Thread(target=self.tray_icon_start, args=(), daemon=True).start()

        self.create_gui_structure()

        if self.root == self.parent:      # if it is independent window (without insertion in outside project)
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
        # ROOT_METHODS
        self.root.title("STAND LAUNCHER")
        self.root.geometry("800x300")   # ("WINXxWINY+ShiftX+ShiftY")
        # self.root.resizable(width=True, height=True)	# заблокировать возможность изменения размеров границ! В том числе на весь экран!!!
        # self.root.maxsize(1000, 1000)
        # self.root.minsize(300, 300)
        # self.root.overrideredirect(False)
        # self.root.state('normal')     # normal/zoomed/iconic/withdrawn
        self.root.iconbitmap(filename_program_image)   # ONLY FILENAME! NO fileobject
        self.root.protocol('WM_DELETE_WINDOW', self.program_exit)  # intersept gui exit()

        # WM_ATTRIBUTES
        # self.root.wm_attributes("-topmost", False)
        # self.root.wm_attributes("-disabled", False)
        # self.root.wm_attributes("-fullscreen", False)
        # self.root.wm_attributes("-transparentcolor", None)

        # WGT_PARAMETERS
        self.root["bg"] = "black"
        self.root["fg"] = None
        # self.root["width"] = None
        # self.root["height"] = None
        # self.root["bind"] = None
        self.root["relief"] = "raised"  # "flat"/"sunken"/"raised"/"groove"/"ridge"
        # self.root["borderwidth"] = 5

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
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure([0, 1, ], weight=0)
        pad_external = 5

        # ======= FRAME-0 (WINDOW CONTROL) ====================
        self.frame_control = Frame(self.parent, bg="#101010")
        self.frame_control.grid(row=0, sticky="nsew", padx=pad_external, pady=pad_external)

        # ======= FRAME-1 (SETTINGS) ====================
        self.frame_settings = Frame(self.parent, bg="#505050", height=30)
        self.frame_settings.pack_propagate(1)   # hear it is necessary
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
        self.btn_window_blank.pack(side="left")

        self.btn_window_switch_to_default = ButtonMod(parent=parent, flag_default=None, bg_default=None, func=self.window_set_default)
        self.btn_window_switch_to_default["text"] = "default"
        self.btn_window_switch_to_default.pack(side="left")

        self.btn_window_short = ButtonMod(parent=parent, flag_default=False, bg_default=None, func=self.window_short)
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

        self.btn_window_moveto00 = ButtonMod(parent=parent, flag_default=None, bg_default=None, func=self.window_move_to_00)
        self.btn_window_moveto00["text"] = chr(8689)
        self.btn_window_moveto00.pack(side="left")

        self.btn_window_topalways = ButtonMod(parent=parent, flag_default=True, bg_default=None, func=self.window_control_topalways)
        self.btn_window_topalways["text"] = "top"
        self.btn_window_topalways.pack(side="left")

        self.btn_window_independent = ButtonMod(parent=parent, flag_default=False, bg_default=None, func=self.window_control_independent)
        self.btn_window_independent["text"] = chr(10043)
        self.btn_window_independent.pack(side="left")

        self.btn_window_settings = ButtonMod(parent=parent, flag_default=False, bg_default=None, func=self.frame_settings_open)
        self.btn_window_settings["text"] = "Настройки"
        self.btn_window_settings.pack(side="left")

    def window_set_default(self):
        for btn_control in ButtonMod.buttonmod_flagged_list:
            btn_control.switch_default()
        self.gui_root_configure()
        self.window_move_to_center()

    def window_short(self, flag=False):
        self.window_control_fullscreen(False)
        window_width = 130       # it does not matter if less then about 120!!!
        window_height = 45
        if flag:
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

    def window_move_to_00(self):
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
        # data_to_save = self.buttons_main_gui_control_data_active
        # with open(filename_program_save_state, 'wb') as file:
        #     pickle.dump(data_to_save, file)
        # print("ok")


class ButtonMod(Button):
    color_off_on = ["white", "#77FF77"]
    buttonmod_flagged_count = 0
    buttonmod_flagged_list = []

    def __init__(self, parent=None, flag_default=None, bg_default=None, func=None):
        super().__init__(parent)
        self.parent = parent

        self.is_flagged = False if flag_default is None else True

        self.bg_set = ButtonMod.color_off_on if bg_default is None else [bg_default, ButtonMod.color_off_on[1]]
        self["bg"] = self.bg_set[0]

        self.func = func if func is not None else lambda flag=False: None
        self["command"] = self.switch

        if self.is_flagged:
            self.flag_default = flag_default
            self.flag_active = flag_default
            ButtonMod.buttonmod_flagged_count += 1
            ButtonMod.buttonmod_flagged_list += [self]
            self.switch_default()

    def switch(self):
        if self.is_flagged:
            self.flag_active = not self.flag_active
            self["bg"] = self.bg_set[int(self.flag_active)]
            self.func(flag=self.flag_active)
        else:
            self.func()

    def switch_default(self):
        if self.is_flagged:
            self.flag_active = not self.flag_default
        self.switch()


def main():
    root = Tk()
    app = Gui(parent=root)
    app.mainloop()


if __name__ == '__main__':
    main()
