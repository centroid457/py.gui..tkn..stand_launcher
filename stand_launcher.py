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
    def __init__(self, master=None):
        self.window_flag_topalways = 0
        self.window_flag_fullscreen = 0
        self.window_flag_independent = 0
        self.button_color_set_normal = ("white", "#77FF77")
        self.window_state = ('normal', "zoomed")

        super().__init__(master)
        self.master = master
        self.pack()
        self.master.title("STAND LAUNCHER")
        self.create_widgets()
        self.window_geometry()

    def window_control_top(self, setdefault=False):
        self.window_flag_topalways = 0 if setdefault else not (self.window_flag_topalways)
        print(self.window_flag_topalways)
        self.button_window_topalways["bg"] = self.button_color_set_normal[int(self.window_flag_topalways)]
        self.master.wm_attributes("-topmost", self.window_flag_topalways)


    def window_control_fullscreen(self, setdefault=False):
        self.window_flag_fullscreen = 0 if setdefault else not (self.window_flag_fullscreen)
        self.button_window_fullscreen["bg"] = self.button_color_set_normal[int(self.window_flag_fullscreen)]
        self.master.state(self.window_state[int(self.window_flag_fullscreen)])
        if not self.window_flag_fullscreen:
            self.master.wm_attributes('-fullscreen', self.window_flag_fullscreen)


    def window_control_independent(self, setdefault=False):
        self.window_flag_independent = 0 if setdefault else not (self.window_flag_independent)
        self.button_window_independent["bg"] = self.button_color_set_normal[int(self.window_flag_independent)]
        self.master.wm_overrideredirect(self.window_flag_independent)


    def window_geometry(self, moveto00=False):
        if moveto00:   # only move to (0,0)
            self.master.geometry("+0+0")
            return


        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 500
        window_height = 200

        x = (screen_width - window_width) / 2
        y = (screen_height - window_height) / 2
        self.master.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

        self.window_control_top(setdefault=True)
        self.window_control_fullscreen(setdefault=True)
        self.window_control_independent(setdefault=True)

    def create_widgets(self):
        # ==================== FRAME CONTROL ====================
        frame_control = tk.Frame(self.master, bg="#505050")
        frame_control.pack(side='top', fill=tk.BOTH, expand=0)
        '''Would Be great if it could be specified to only be moved
        when dragging with the Frame above.'''
        grip = Grip(frame_control)

        # -------------------- BUTTONS --------------------
        self.button_window_exit = tk.Button(frame_control,
                                    text="X", width=3, height=1,
                                    bg="#FF3333", fg="white",
                                    command=lambda: exit())
        self.button_window_exit.pack(side='left')

        self.button_window_fullscreen = tk.Button(frame_control,
                                          text="^", width=3, height=1,
                                          bg=self.button_color_set_normal[int(self.window_flag_fullscreen)], fg="black",
                                          command=self.window_control_fullscreen)
        self.button_window_fullscreen.pack(side='left')

        self.button_window_down = tk.Button(frame_control,
                                    text="_", width=3, height=1,
                                    bg="white", fg="black",
                                    command=lambda: self.master.iconify())
        self.button_window_down.pack(side='left')

        self.button_window_moveto00 = tk.Button(frame_control,
                                         text="(0.0)", width=3, height=1,
                                         bg=self.button_color_set_normal[int(self.window_flag_topalways)], fg="black",
                                         command=lambda:self.window_geometry(moveto00=True))
        self.button_window_moveto00.pack(side='left')

        self.button_window_make_fullscreen = tk.Button(frame_control,
                                         text="begin", height=1,
                                         bg=self.button_color_set_normal[int(self.window_flag_topalways)], fg="black",
                                         command=lambda:self.window_geometry())
        self.button_window_make_fullscreen.pack(side='left')

        self.button_window_topalways = tk.Button(frame_control,
                                         text="top", width=3, height=1,
                                         bg=self.button_color_set_normal[int(self.window_flag_topalways)], fg="black",
                                         command=self.window_control_top)
        self.button_window_topalways.pack(side='left')

        self.button_window_independent = tk.Button(frame_control,
                                              text="I", width=3, height=1,
                                              bg=self.button_color_set_normal[int(self.window_flag_independent)],
                                              fg="black",
                                           command=self.window_control_independent)
        self.button_window_independent.pack(side='left')

        self.button_window_settings = tk.Button(frame_control,
                                        text="Настройки", height=1,
                                        bg="white", fg="black",
                                        command=lambda: None)
        self.button_window_settings.pack(side='left')


        # ==================== FRAME MAIN ====================
        self.frame_back = tk.Frame(self.master, bg="grey")
        self.frame_back.pack_propagate(0)
        self.frame_back.pack(side='top', fill=tk.BOTH, expand=1)


def main():
    root = tk.Tk()
    app = Gui(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()