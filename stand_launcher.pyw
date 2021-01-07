# DO NOT USE ANY PRINT() FUNCTIONS! ONLY for debug purpose!! else it will brake program_restart()!

# #################################################
# LIBS
# #################################################

import os
import sys
import pickle
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

filename_check_program_instances_prefix = ".started_"
filename_check_program_instances_suffix = "_instance.check"

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
    def __init__(self, root=None):
        super().__init__()
        self.root = root
        if not self.check_program_instances():
            self.window_state = ('normal', "zoomed")
            self.create_icon()

            Thread(target=self.tray_icon_start, args=(), daemon=True).start()

            self.gui_general_configure()
            self.create_gui_structure()
            self.create_gui_geometry()

    def __del__(self):
        print("execute destructor")
        self.program_save_state()

    def check_program_instances(self):
        mask = f"{str(dirname_settings)}" + '\\'\
                    f"{filename_check_program_instances_prefix}"\
                    f"*{filename_check_program_instances_suffix}"
        print(mask)
        if len(glob(mask)):
            print("Program already have earlier started instance. Can't start new one!", file=sys.stderr)
            self.program_exit()
            return True
        self.temporary_file = NamedTemporaryFile(
            suffix=filename_check_program_instances_suffix,
            prefix=filename_check_program_instances_prefix,
            dir=dirname_settings)

    def gui_general_configure(self):
        self.root.title("STAND LAUNCHER")
        self.root.iconbitmap(filename_program_image)
        self.root.protocol('WM_DELETE_WINDOW', self.program_exit)  # intersept gui exit()
        self.root["bg"] = "black"

    def create_gui_geometry(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 800
        window_height = 200
        x = (screen_width - window_width) / 2
        y = (screen_height - window_height) / 2
        self.root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

        self.load_gui_settings()

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
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure([1, 2], weight=0)
        self.root.rowconfigure(3, weight=1)
        pad_external = 10

        # ======= FRAME-1 (WINDOW CONTROL) ====================
        self.frame_control = Frame(self.root, bg="#101010")
        self.frame_control.grid(row=1, sticky="nsew", padx=pad_external, pady=pad_external)
        Make_gui_draggable(self.root)
        self.create_gui_control_buttons(self.frame_control)

        # ======= FRAME-2 (SETTINGS) ====================
        self.frame_settings = Frame(self.root, bg="#505050", height=30)
        self.frame_settings.pack_propagate(0)   # hear it is necessary
        self.frame_settings.grid(row=2, sticky="ew", padx=pad_external, pady=0)
        self.create_settings_aria(self.frame_settings)

        # ======= FRAME-3 (MAIN WORK SET) ====================
        self.frame_main_work = Frame(self.root, bg="grey")
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

    def create_settings_aria(self, root):
        self.create_null_label(root)

    def create_work_menu(self, root):
        self.create_null_label(root)

    def create_work_aria(self, root):
        self.create_null_label(root)

    def create_work_error_eria(self, root):
        self.create_null_label(root)

    def create_null_label(self, root):
        self.label_null = Label(root, text="ПУСТО", fg="white", bg="#505050")
        self.label_null.pack(side="left", fill="x", expand=0)

    # #################################################
    # BUTTONS
    # #################################################
    def load_gui_settings(self, set_default=False):
        if not set_default and os.path.exists(filename_program_save_state):
            with open(filename_program_save_state, 'rb') as file:
                self.buttons_main_gui_control_data_active = pickle.load(file)
        else:
            self.buttons_main_gui_control_data_active = self.get_gui_default()

    def get_gui_default(self):
        colorset_button_normal = ["white", "#77FF77"]
        self.button_switch_window_to_default_name = "default"   # button_name wich make window as default state!
        buttons_main_gui_control_data_default = {
            "button_window_blank": {
                "flag": None,
                "text": chr(9995),
                "bg": ["white"],
                "command": lambda flag: None,
            },
            "button_window_switch_to_default": {
                "flag": None,
                "text": self.button_switch_window_to_default_name,
                "bg": ["white"],
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
                "bg": ["white"],
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
                "bg": ["white"],
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
            "button_window_settings": {
                "flag": False,
                "text": "Настройки",
                "bg": colorset_button_normal,
                "command": lambda flag: self.frame_settings_open(flag=flag),
            },
        }
        return buttons_main_gui_control_data_default

    def create_gui_control_buttons(self, frame):
        self.load_gui_settings()
        for button_id in self.buttons_main_gui_control_data_active:
            button_obj = Button(frame)
            button_data = self.buttons_main_gui_control_data_active[button_id]
            button_obj["text"] = button_data["text"]
            if button_obj["text"] == "":       # disable blank buttons
                button_obj["state"] = "disabled"
            button_obj["width"] = 3 if len(button_data["text"]) < 3 else None
            button_obj["bg"] = button_data["bg"][0]
            button_obj.bind("<Button-1>", self.buttons_handler)
            button_obj.pack(side="left")

    def buttons_handler(self, event):
        for button_id in self.buttons_main_gui_control_data_active:
            # finding data line corresponding to pressed button
            button_data = self.buttons_main_gui_control_data_active[button_id]
            if button_data["text"] == event.widget["text"]:
                # if find - use data
                if button_data["text"] == self.button_switch_window_to_default_name:
                    # if fined the special button just execute its lambda!
                    button_data["command"](widget=event.widget)
                    return

                # CHANGE FLAG
                flag_old = button_data["flag"]
                if flag_old is not None:
                    flag_new = not flag_old
                    button_data["flag"] = flag_new
                    # CHANGE windget
                    event.widget["bg"] = button_data["bg"][flag_new]
                else:
                    flag_new = None

                # EXECUTE COMMAND
                button_data["command"](flag=flag_new)
                # EXIT for-cycle
                return      # do not delete!

    # BUTTON FUNCTIONS
    def gui_apply_settings(self):
        #self.widgets_all_iter()
        self.window_control_fullscreen(flag=False)
        self.window_control_top(flag=False)
        self.window_control_independent(flag=False)
        self.frame_settings_open(flag=False)

    def widgets_all_iter(self, my_frame=None, level="."):
        if my_frame == None:
            my_frame = self.root
        frame_childrens = my_frame.children
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
        self.gui_apply_settings()
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

        self.gui_apply_settings()
        self.create_gui_geometry()

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

def main():
    root = Tk()
    app = Gui(root=root)
    app.mainloop()


if __name__ == '__main__':
    main()
