# DO NOT USE ANY PRINT() FUNCTIONS! ONLY for debug purpose!! else it will brake program_restart()!

# #################################################
# LIBS
# #################################################
import os
import sys
import pathlib

from glob import glob
from time import sleep
from tkinter import Tk, Frame, Button, Label, BOTH
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
        self.root = parent.winfo_toplevel()
        Make_gui_draggable(self.root)

        self.check_program_instances()
        self.window_state = ('normal', "zoomed")
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
            print("Program already have earlier started instance. Can't start new one!", file=sys.stderr)
            self.program_exit()
            return
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
        self.root.geometry("800x300")   #("WINXxWINY+ShiftX+ShiftY")
        #self.root.resizable(width=True, height=True)	# заблокировать возможность изменения размеров границ! В том числе на весь экран!!!
        #self.root.maxsize(1000, 1000)
        #self.root.minsize(300, 300)
        #self.root.overrideredirect(False)
        #self.root.state('normal')     # normal/zoomed/iconic/withdrawn
        self.root.iconbitmap(filename_program_image)   #=ONLY FILENAME! NO fileobject
        self.root.protocol('WM_DELETE_WINDOW', self.program_exit)  # intersept gui exit()

        # WM_ATTRIBUTES
        self.root.wm_attributes("-topmost", False)
        self.root.wm_attributes("-disabled", False)
        self.root.wm_attributes("-fullscreen", False)
        self.root.wm_attributes("-transparentcolor", None)

        # WGT_PARAMETERS
        self.root["bg"] = "black"
        self.root["fg"] = None
        #self.root["width"] = None
        #self.root["height"] = None
        #self.root["bind"] = None
        self.root["relief"] = "raised"  # "flat"/"sunken"/"raised"/"groove"/"ridge"
        #self.root["borderwidth"] = 5

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

    def tray_action_show_gui(self, tray_icon_obj_infunc, MenuItem):
        self.root.deiconify()

    def tray_action_exit(self, tray_icon_obj_infunc, MenuItem):
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

        self.create_gui_control_buttons(self.frame_control)

        # ======= FRAME-1 (SETTINGS) ====================
        self.frame_settings = Frame(self.parent, bg="#505050", height=30)
        self.frame_settings.pack_propagate(1)   # hear it is necessary
        self.frame_settings.grid(row=1, sticky="ew", padx=pad_external, pady=0)
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
        colorset_button_normal = ["white", "#77FF77"]
        '''
        {
            "button_window_switch_to_default": {
                "flag": None,
                "text": '123',
                "bg": colorset_button_normal,
                "command": lambda widget: self.window_set_default(widget=widget),
            },
            "button_window_short": {
                "flag": False,
                "text": chr(9624),
                "bg": colorset_button_normal,
                "command": lambda flag: self.window_short(flag=flag),
            },
            "button_window_exit": {             # first level it's only id! you can change it any time
                "flag": None,                   # None mean it will always do the same things, flag not used
                "text": chr(9587),              # text on the button
                "bg": ["#FF6666"],       # second color is for flaged button state, it will rotating
                "command": lambda flag: self.program_exit(),
            },
            "button_window_fullscreen": {
                "flag": False,
                "text": chr(9744),
                "bg": colorset_button_normal,
                "command": lambda flag: self.window_control_fullscreen(flag=flag),
            },
            "button_window_minimize": {
                "flag": None,
                "text": "_",
                "bg": colorset_button_normal,
                "command": lambda flag: self.window_control_minimize(),
            },
            "button_program_restart": {
                "flag": None,
                "text": "restart",
                "bg": ["#FF6666"],
                "command": lambda flag: self.program_restart(),
            },
            "button_window_moveto00": {
                "flag": None,
                "text": chr(8689),
                "bg": colorset_button_normal,
                "command": lambda flag: self.window_move_to_00(),
            },
            "button_window_topalways": {
                "flag": False,
                "text": "top",
                "bg": colorset_button_normal,
                "command": lambda flag: self.window_control_top(flag=flag),
            },
            "button_window_independent": {
                "flag": False,
                "text": chr(10043),
                "bg": colorset_button_normal,
                "command": lambda flag: self.window_control_independent(flag=flag),
            },
        }
            def __init__(self, parent=None, flagged=False, flag_default=False, bg_default=None):

        '''









        self.btn_window_blank = ButtonMod(parent=parent, flagged=False, flag_default=False, bg_default=None, func=None)
        self.btn_window_blank["text"] = chr(9995)
        self.btn_window_blank.pack(side="left")

        self.btn_window_settings = ButtonMod(parent=parent, flagged=True, flag_default=True, bg_default=None, func=self.frame_settings_open)
        self.btn_window_settings["text"] = "Настройки"
        self.btn_window_settings.pack(side="left")
        #self.btn_window_settings.func(None)
        #self.btn_window_settings.switch()
        self.btn_window_settings.set_default_state()
        print(self.btn_window_settings.flag_active)


    def widgets_all_iter(self, parent=None, level="."):
        if parent == None:
            parent = self.root
        frame_childrens = parent.children
        for wgt in frame_childrens:
            wgt_current_name = wgt
            if wgt[0:6] == "!frame":
                print(level + wgt_current_name)
                widgets_all_iter(my_frame=frame_childrens[wgt], level=level + wgt_current_name)

            elif wgt[0:7] == "!button":
                print(level + wgt_current_name)
                change_widget(frame_childrens[wgt])

    def window_move_to_00(self):
        self.root.geometry("+0+0")

    def window_short(self, flag=False):
        self.window_control_fullscreen(False)
        window_width = 130       # it does not matter if less then about 120!!!
        window_height = 45
        if flag:
            self.root.geometry('%dx%d+%d+%d' % (window_width, window_height, 0, 0))

    def window_control_fullscreen(self, flag=False):
        self.root.state(self.window_state[int(flag)])
        if not flag:
            self.root.wm_attributes('-fullscreen', flag)

    def window_control_minimize(self):
        if not self.buttons_main_gui_control_data_active["button_window_independent"]["flag"]:
            self.root.iconify()
        else:
            self.root.withdraw()

    def window_control_top(self, flag=False):
        self.root.wm_attributes("-topmost", flag)

    def window_set_default(self, widget):
        self.load_gui_settings(set_default=True)
        return
        remaining_buttons_to_reset = self.buttons_main_gui_control_data_active.copy()

        parent_widget_name = widget.winfo_parent()      # .!frame
        parent_widget_obj = widget._nametowidget(parent_widget_name)
        button_obj_list = parent_widget_obj.pack_slaves()

        for widget_obj in button_obj_list:
            for button_id in remaining_buttons_to_reset:
                if remaining_buttons_to_reset[button_id]["text"] == widget_obj["text"]:
                    poped_button = remaining_buttons_to_reset.pop(button_id)
                    widget_obj["bg"] = poped_button["bg"][0]
                    break

        self.create_gui_geometry()

    def window_control_independent(self, flag=False):
        """make window independent from OS explorer"""
        self.root.wm_overrideredirect(flag)

    def frame_settings_open(self, flag=False):
        print("FUNC GET SELF", self)
        print("FUNC GET FLAG", flag)
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
        # If you want to work with correct restart button DO NOT USE ANY PRINT-function befor!!!!
        # else programm will not actually restart (in PyCharm will not start after second Restart)
        os.execl(python_exe, python_exe, *sys.argv)

    def program_exit(self):
        self.program_save_state()
        print("exit")
        self.root.destroy()

    def program_save_state(self, data_to_save=None):
        pass
        #data_to_save = self.buttons_main_gui_control_data_active
        #with open(filename_program_save_state, 'wb') as file:
            #pickle.dump(data_to_save, file)
        #print("ok")


class ButtonMod(Button):
    color_flag_off_on = ["white", "#77FF77"]
    flagged_buttons_count = 0
    flagged_buttons_list = []

    def __init__(self1, parent=None, flagged=False, flag_default=False, bg_default=None, func=None):
        super().__init__(parent)
        self1.parent = parent
        self1.is_flagged = flagged
        self1.flag_default = flag_default
        self1.flag_active = flag_default
        self1.bg_set = ButtonMod.color_flag_off_on if bg_default is None else [bg_default, ButtonMod.color_flag_off_on[1]]
        self1.func = func if func is not None else lambda flag=False: None
        self1["command"] = self1.switch
        print(self1, self1["text"], self1.flag_active)
        #self1.func()


        if self1.is_flagged == True:
            ButtonMod.flagged_buttons_count += 1
            ButtonMod.flagged_buttons_list += [self1]
            #self1.switch_default()
            #self1.switch()
        else:
            pass #self1["command"] = self1.func


    def switch(self1):
        if self1.is_flagged == True:
            self1.flag_active = not self1.flag_active
            self1["bg"] = self1.bg_set[int(self1.flag_active)]

        print(self1["text"], self1.flag_active)
        self1.func(flag=self1.flag_active)

    def switch_default(self1):
        self1.flag_active = not self1.flag_default
        self1.switch()

    def set_default_state(self1):
        self1.flag_active = self1.flag_default
        self1["bg"] = self1.bg_set[int(self1.flag_active)]


def main():
    root = Tk()
    app = Gui(parent=root)
    app.mainloop()


if __name__ == '__main__':
    main()
