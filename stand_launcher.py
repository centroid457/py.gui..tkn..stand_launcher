import tkinter as tk


class Grip:
    ''' Makes a window dragable by mouse '''
    def __init__ (self, parent, disable=None, releasecmd=None) :
        self.parent = parent
        self.root = parent.winfo_toplevel()

        self.disable = disable
        if type(disable) == 'str':
            self.disable = disable.lower()

        self.releaseCMD = releasecmd

        self.parent.bind('<Button-1>', self.relative_position)
        self.parent.bind('<ButtonRelease-1>', self.drag_unbind)


    def relative_position (self, event) :
        cx, cy = self.parent.winfo_pointerxy()
        geo = self.root.geometry().split("+")
        self.oriX, self.oriY = int(geo[1]), int(geo[2])
        self.relX = cx - self.oriX
        self.relY = cy - self.oriY

        self.parent.bind('<Motion>', self.drag_wid)


    def drag_wid (self, event) :
        cx, cy = self.parent.winfo_pointerxy()
        d = self.disable
        x = cx - self.relX
        y = cy - self.relY
        if d == 'x' :
            x = self.oriX
        elif d == 'y' :
            y = self.oriY
        self.root.geometry('+%i+%i' % (x, y))


    def drag_unbind (self, event) :
        self.parent.unbind('<Motion>')
        if self.releaseCMD != None :
            self.releaseCMD()


class Gui(tk.Frame):
    """ main GUI window """
    def __init__(self, master=None):
        self.window_flag_topalways = False
        self.window_flag_fullscreen = False
        self.window_flag_independent = False
        self.window_flag_frame_settings_open = False
        self.color_button_set_normal = ("white", "#77FF77")
        self.window_state = ('normal', "zoomed")

        super().__init__(master)
        self.master = master
        self.master.title("STAND LAUNCHER")
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

        self.window_control_top(setdefault=True)
        self.window_control_fullscreen(setdefault=True)
        self.window_control_independent(setdefault=True)
        self.frame_settings_open(setdefault=True)


    def create_gui_structure(self):
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure([1,2], weight=0)
        self.master.rowconfigure(3, weight=1)

        # ======= FRAME-1 (WINDOW CONTROL) ====================
        self.frame_control = tk.Frame(self.master, bg="#505050")
        self.frame_control.grid(row=1, sticky="nsew", padx=1, pady=1)
        '''Would Be great if it could be specified to only be moved
        when dragging with the Frame above.'''
        grip = Grip(self.frame_control)
        self.create_control_buttons(self.frame_control)


        # ======= FRAME-2 (SETTINGS) ====================
        self.frame_settings = tk.Frame(self.master, bg="#505050", height=30)
        self.frame_settings.pack_propagate(0)   # hear it is necessary
        self.frame_settings.grid(row=2, sticky="ew", padx=1, pady=1)
        self.create_settings_aria(self.frame_settings)


        # ======= FRAME-3 (MAIN WORK SET) ====================
        self.frame_main_work = tk.Frame(self.master, bg="grey")
        self.frame_main_work.grid(row=3, sticky="snew", padx=1, pady=1)

        # ------- FRAME-3 /1 frame LEFT-main menu -----------------
        self.frame_menu_left = tk.Frame(self.frame_main_work, bg="grey", width=200, height=100)
        self.frame_menu_left.pack(side='left', fill=tk.BOTH, expand=0, padx=1, pady=1)
        self.frame_menu_left.pack_propagate(0)
        self.create_work_menu(self.frame_menu_left)

        # ------- FRAME-1 /2 frame CENTER-main work aria -----------------
        self.frame_work_aria = tk.Frame(self.frame_main_work, bg="#ffffff", width=200)
        self.frame_work_aria.pack(side='left', fill=tk.BOTH, expand=1, padx=1, pady=1)
        self.frame_work_aria.pack_propagate(0)
        self.create_work_aria(self.frame_work_aria)

        # ------- FRAME-1 /3 frame RIGHT-error aria -----------------
        self.frame_error_aria = tk.Frame(self.frame_main_work, bg="grey", width=200)
        self.frame_error_aria.pack(side='left', fill=tk.BOTH, expand=0, padx=1, pady=1)
        self.frame_error_aria.pack_propagate(0)
        self.create_work_error_eria(self.frame_error_aria)


    def get_button_data(self):
        self.button_data = {
            "button_window_exit":{
                "text" : "X",
                "bg" : "#FF6666",
                "command" : exit,
                "side" : "left",
                },

            "button_window_fullscreen":{
                "text": "^",
                "bg": self.color_button_set_normal[int(self.window_flag_fullscreen)],
                "command": self.window_control_fullscreen,
                "side": "left",
                },

            "button_window_down":{
                "text": "_",
                "bg": "white",
                "command": lambda: self.master.iconify(),
                "side": "left",
                },

            "button_window_moveto00": {
                "text": "(0.0)",
                "bg": self.color_button_set_normal[int(self.window_flag_topalways)],
                "command": lambda: self.create_window_geometry(moveto00=True),
                "side": "left",
                },

            "button_window_set_as_started": {
                "text": "begin",
                "bg": self.color_button_set_normal[int(self.window_flag_topalways)],
                "command": self.create_window_geometry,
                "side": "left",
                },

            "button_window_topalways": {
                "text": "top",
                "bg": self.color_button_set_normal[int(self.window_flag_topalways)],
                "command": self.window_control_top,
                "side": "left",
                },

            "button_window_independent": {
                "text": "I",
                "bg": self.color_button_set_normal[int(self.window_flag_independent)],
                "command": self.window_control_independent,
                "side": "left",
                },

            "button_window_settings": {
                "text": "Настройки",
                "bg": "white",
                "command": self.frame_settings_open,
                "side": "left",
                },
            }

    def create_control_buttons(self, master):
        self.get_button_data()
        for i in self.button_data:
            self.create_button(master, i)

    def create_button(self, frame, button_type):
        btn = tk.Button(frame)
        btn["text"]=self.button_data[button_type]["text"]
        btn["width"]=3 if len(btn["text"]) < 3 else None
        btn["bg"]=self.button_data[button_type]["bg"]
        btn.bind("<Button-1>", self.buttons_handle)
        btn.pack(side=self.button_data[button_type]['side'])

    def buttons_handle(self, event):
        for button_id in self.button_data:
            if self.button_data[button_id]["text"] == event.widget["text"]:
                self.button_data[button_id]["command"]()
                return

    # BUTTON FUNCTIONS
    def window_control_top(self, setdefault=False):
        self.window_flag_topalways = 0 if setdefault else not (self.window_flag_topalways)
        #self.button_window_topalways["bg"] = self.color_button_set_normal[int(self.window_flag_topalways)]
        self.master.wm_attributes("-topmost", self.window_flag_topalways)

    def window_control_fullscreen(self, setdefault=False):
        self.window_flag_fullscreen = 0 if setdefault else not (self.window_flag_fullscreen)
        #self.button_window_fullscreen["bg"] = self.color_button_set_normal[int(self.window_flag_fullscreen)]
        self.master.state(self.window_state[int(self.window_flag_fullscreen)])
        if not self.window_flag_fullscreen:
            self.master.wm_attributes('-fullscreen', self.window_flag_fullscreen)

    def window_control_independent(self, setdefault=False):
        """make window independent from OS explorer"""
        self.window_flag_independent = 0 if setdefault else not (self.window_flag_independent)
        #self.button_window_independent["bg"] = self.color_button_set_normal[int(self.window_flag_independent)]
        self.master.wm_overrideredirect(self.window_flag_independent)

    def frame_settings_open(self, setdefault=False):
        self.window_flag_frame_settings_open = 0 if setdefault else not (self.window_flag_frame_settings_open)
        #self.button_window_settings["bg"] = self.color_button_set_normal[int(self.window_flag_frame_settings_open)]
        if self.window_flag_frame_settings_open:
            self.frame_settings.grid()
        else:
            self.frame_settings.grid_remove()



    def create_settings_aria(self, master):
        self.create_null_label(master)

    def create_work_menu(self, master):
        self.create_null_label(master)

    def create_work_aria(self, master):
        self.create_null_label(master)

    def create_work_error_eria(self, master):
        self.create_null_label(master)


    def create_null_label(self, master):
        self.label_null = tk.Label(master, text="ПУСТО", fg="white", bg="#505050")
        self.label_null.pack(side="left", fill="x", expand=0)

def main():
    root = tk.Tk()
    app = Gui(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()