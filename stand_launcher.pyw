# DO NOT USE ANY PRINT() FUNCTIONS! ONLY for debug purpose!! else it will brake program_restart()!

# #################################################
# LIBS
# #################################################
import os
import sys

from glob import glob
from time import sleep
from tkinter import Tk, Frame, Button, Label, BOTH
from tempfile import NamedTemporaryFile
from threading import Thread
from collections import deque

# NEED TO INSTALL
from PIL import Image, ImageDraw, ImageFont     # pip3 install pillow
from pystray import Icon, Menu, MenuItem        # pip3 install pystray

# #################################################
# SETTINGS
# #################################################
folder_for_auxiliary_project_files_wo_slashes = "settings"
if not os.path.isdir(folder_for_auxiliary_project_files_wo_slashes):
    os.mkdir(folder_for_auxiliary_project_files_wo_slashes)

program_image_name = folder_for_auxiliary_project_files_wo_slashes + "/program_icon.ico"


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
    def __init__(self, master=None):
        super().__init__(master)
        self.check_program_instances()
        self.master = master
        self.window_state = ('normal', "zoomed")
        self.create_icon()

        Thread(target=self.tray_icon_start, args=(), daemon=True).start()

        self.gui_general_configure()
        self.create_gui_structure()
        self.create_gui_geometry()

    def gui_general_configure(self):
        self.master.title("STAND LAUNCHER")
        self.master.iconbitmap(program_image_name)
        self.master.protocol('WM_DELETE_WINDOW', self.program_exit)  # intersept gui exit()
        self.master["background"] = "black"

    def create_gui_geometry(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 800
        window_height = 200
        x = (screen_width - window_width) / 2
        y = (screen_height - window_height) / 2
        self.master.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

        self.window_set_default_all_functions()


    def __del__(self):
        self.program_save_state()

    def check_program_instances(self):
        prefix = ".started_"
        suffix = "_instance.check"
        dir_current = os.path.dirname(__file__)
        dir_destination = dir_current + "/" + folder_for_auxiliary_project_files_wo_slashes + "/"
        if len(glob(f"{dir_destination}{prefix}*{suffix}")):
            print("Program already have earlier started instance. Can't start new one!", file=sys.stderr)
            sys.exit()
        self.temporary_file = NamedTemporaryFile(suffix=suffix, prefix=prefix, dir=dir_destination)

    # #################################################
    # TRAY
    # #################################################
    def create_icon(self):
        if os.path.exists(program_image_name):
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
        image_obj.save(program_image_name)
        return

    def tray_icon_start(self):
        tray_icon_obj = Icon('tray name')
        tray_icon_obj.icon = Image.open(program_image_name)
        menu = Menu(
            MenuItem(text='РАСКРЫТЬ', action=self.tray_action_show_gui, default=True),
            MenuItem(text='ВЫХОД', action=self.tray_action_exit)
        )
        tray_icon_obj.menu = menu
        tray_icon_obj.run()

    def tray_action_show_gui(self, tray_icon_obj_infunc, MenuItem):
        self.master.deiconify()

    def tray_action_exit(self, tray_icon_obj_infunc, MenuItem):
        self.master.destroy()
        # program_exit()     # still not working!


    # #################################################
    # FRAMES
    # #################################################
    def create_gui_structure(self):
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure([1, 2], weight=0)
        self.master.rowconfigure(3, weight=1)
        pad_external = 10

        # ======= FRAME-1 (WINDOW CONTROL) ====================
        self.frame_control = Frame(self.master, bg="#101010")
        self.frame_control.grid(row=1, sticky="nsew", padx=pad_external, pady=pad_external)
        Make_gui_draggable(self.master)
        self.create_control_buttons(self.frame_control)

        # ======= FRAME-2 (SETTINGS) ====================
        self.frame_settings = Frame(self.master, bg="#505050", height=30)
        self.frame_settings.pack_propagate(0)   # hear it is necessary
        self.frame_settings.grid(row=2, sticky="ew", padx=pad_external, pady=0)
        self.create_settings_aria(self.frame_settings)

        # ======= FRAME-3 (MAIN WORK SET) ====================
        self.frame_main_work = Frame(self.master, bg="grey")
        self.frame_main_work.grid(row=3, sticky="snew", padx=pad_external, pady=pad_external)

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
    def set_default_buttons_data(self):
        color_button_normal_set = ["white", "#77FF77"]
        self.button_switch_window_to_default_name = "default"   # button_name wich make window as default state!
        buttons_data_default = {
            "button_window_blank": {
                "flag": None,
                "text": chr(9995),
                "bg": deque(["white"]),
                "command": lambda flag: None,
            },
            "button_window_switch_to_default": {
                "flag": None,
                "text": self.button_switch_window_to_default_name,
                "bg": deque(["white"]),
                "command": lambda widget: self.window_set_default(widget=widget),
            },
            "button_window_short": {
                "flag": False,
                "text": chr(9624),
                "bg": deque(color_button_normal_set),
                "command": lambda flag: self.window_short(flag=flag),
            },
            "button_window_exit": {             # first level it's only id! you can change it any time
                "flag": None,                   # None mean it will always do the same things, flag not used
                "text": chr(9587),              # text on the button
                "bg": deque(["#FF6666"]),       # second color is for flaged button state, it will rotating
                "command": lambda flag: self.program_exit(),
            },
            "button_window_fullscreen": {
                "flag": False,
                "text": chr(9744),
                "bg": deque(color_button_normal_set),
                "command": lambda flag: self.window_control_fullscreen(flag=flag),
            },
            "button_window_minimize": {
                "flag": None,
                "text": "_",
                "bg": deque(["white"]),
                "command": lambda flag: self.window_control_minimize(),
            },
            "button_program_restart": {
                "flag": None,
                "text": "restart",
                "bg": deque(["#FF6666"]),
                "command": lambda flag: self.program_restart(),
            },
            "button_window_moveto00": {
                "flag": None,
                "text": chr(8689),
                "bg": deque(["white"]),
                "command": lambda flag: self.window_move_to_00(),
            },
            "button_window_topalways": {
                "flag": False,
                "text": "top",
                "bg": deque(color_button_normal_set),
                "command": lambda flag: self.window_control_top(flag=flag),
            },
            "button_window_independent": {
                "flag": False,
                "text": chr(10043),
                "bg": deque(color_button_normal_set),
                "command": lambda flag: self.window_control_independent(flag=flag),
            },
            "button_window_settings": {
                "flag": False,
                "text": "Настройки",
                "bg": deque(color_button_normal_set),
                "command": lambda flag: self.frame_settings_open(flag=flag),
            },
        }
        self.buttons_data_active = buttons_data_default

    def create_control_buttons(self, master):
        self.set_default_buttons_data()
        for button_id in self.buttons_data_active:
            self.create_button(master, button_id)

    def create_button(self, frame, button_id):
        btn = Button(frame)
        btn["text"] = self.buttons_data_active[button_id]["text"]
        if btn["text"] == "":       # disable blank buttons
            btn["state"] = "disabled"
        btn["width"] = 3 if len(btn["text"]) < 3 else None
        btn["bg"] = self.buttons_data_active[button_id]["bg"][0]
        btn.bind("<Button-1>", self.buttons_handle)
        btn.pack(side="left")

    def buttons_handle(self, event):
        for button_id in self.buttons_data_active:
            # finding data line corresponding to pressed button
            if self.buttons_data_active[button_id]["text"] == event.widget["text"]:
                # if find - use data
                if self.buttons_data_active[button_id]["text"] == self.button_switch_window_to_default_name:
                    # if fined the special button just execute its lambda!
                    self.buttons_data_active[button_id]["command"](widget=event.widget)
                    return

                # ROTATE data: FLAG and BG
                self.buttons_data_active[button_id]["bg"].rotate(1)
                flag_old = self.buttons_data_active[button_id]["flag"]
                flag_new = None if flag_old is None else not flag_old
                self.buttons_data_active[button_id]["flag"] = flag_new

                # CHANGE rotated data in windget
                event.widget["bg"] = self.buttons_data_active[button_id]["bg"][0]
                self.buttons_data_active[button_id]["command"](flag=flag_new)
                return

    # BUTTON FUNCTIONS
    def window_set_default_all_functions(self):
        self.set_default_buttons_data()
        self.window_control_fullscreen(flag=False)
        self.window_control_top(flag=False)
        self.window_control_independent(flag=False)
        self.frame_settings_open(flag=False)

    def window_move_to_00(self):
        self.master.geometry("+0+0")

    def window_short(self, flag=False):
        self.window_control_fullscreen(False)
        window_width = 130       # it does not matter if less then about 120!!!
        window_height = 45
        if flag:
            self.master.geometry('%dx%d+%d+%d' % (window_width, window_height, 0, 0))

    def window_control_fullscreen(self, flag=False):
        self.master.state(self.window_state[int(flag)])
        if not flag:
            self.master.wm_attributes('-fullscreen', flag)

    def window_control_minimize(self):
        if not self.buttons_data_active["button_window_independent"]["flag"]:
            self.master.iconify()
        else:
            self.master.withdraw()

    def window_control_top(self, flag=False):
        self.master.wm_attributes("-topmost", flag)

    def window_set_default(self, widget):
        self.set_default_buttons_data()
        remaining_buttons_to_reset = self.buttons_data_active.copy()

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
        self.create_gui_geometry()

    def window_control_independent(self, flag=False):
        """make window independent from OS explorer"""
        self.master.wm_overrideredirect(flag)

    def frame_settings_open(self, flag=False):
        if flag:
            self.frame_settings.grid()
        else:
            self.frame_settings.grid_remove()

    def program_restart(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        self.program_save_state()
        python_exe = sys.executable
        # почему-то если использовать такую конструкцию - НЕЛЬЗЯ ЧТОЛИБО ВЫВОДИТЬ ЧЕРЕЗ PRINT!!!!
        os.execl(python_exe, python_exe, *sys.argv)

    def program_exit(self):
        self.program_save_state()
        print("correct exit")
        sys.exit()

    def program_save_state(self, save_data=None):
        pass

def main():
    root = Tk()
    app = Gui(master=root)
    app.mainloop()


if __name__ == '__main__':
    main()
