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

        super().__init__(master)
        self.master = master
        self.pack()
        self.master.title("STAND LAUNCHER")
        self.window_geometry()
        self.create_widgets()


    def window_control_top(self):
        self.window_flag_topalways = not (self.window_flag_topalways)
        self.master.wm_attributes("-topmost", self.window_flag_topalways)
        self.button_window_topalways["bg"] = self.button_color_set_normal[int(self.window_flag_topalways)]

    def window_control_fullscreen(self):
        self.window_flag_fullscreen = not (self.window_flag_fullscreen)
        self.master.attributes('-fullscreen', self.window_flag_fullscreen)
        self.button_window_fullscreen["bg"] = self.button_color_set_normal[int(self.window_flag_fullscreen)]

    def window_control_independent(self):
        self.window_flag_independent = not (self.window_flag_independent)
        self.master.overrideredirect(self.window_flag_independent)
        self.button_window_independent["bg"] = self.button_color_set_normal[int(self.window_flag_independent)]

    def window_geometry(self):
        w = 300
        h = 200

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

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
        self.button_window_exit.pack(side='right')

        self.button_window_fullscreen = tk.Button(frame_control,
                                          text="^", width=3, height=1,
                                          bg=self.button_color_set_normal[int(self.window_flag_fullscreen)], fg="black",
                                          command=self.window_control_fullscreen)
        self.button_window_fullscreen.pack(side='right')

        self.button_window_down = tk.Button(frame_control,
                                    text="_", width=3, height=1,
                                    bg="white", fg="black",
                                    command=lambda: self.master.iconify())
        self.button_window_down.pack(side='right')

        self.button_window_topalways = tk.Button(frame_control,
                                         text="top", width=3, height=1,
                                         bg=self.button_color_set_normal[int(self.window_flag_topalways)], fg="black",
                                         command=self.window_control_top)
        self.button_window_topalways.pack(side='right')

        self.button_window_independent = tk.Button(frame_control,
                                              text="I", width=3, height=1,
                                              bg=self.button_color_set_normal[int(self.window_flag_independent)],
                                              fg="black",
                                           command=self.window_control_independent)
        self.button_window_independent.pack(side='right')

        self.button_window_settings = tk.Button(frame_control,
                                        text="Настройки", height=1,
                                        bg="white", fg="black",
                                        command=lambda: None)
        self.button_window_settings.pack(side='right')


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