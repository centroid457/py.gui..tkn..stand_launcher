from tkinter import *

class Grip:
    ''' Makes a window dragable. '''
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

def main():
    root = Tk()
    root.title("STAND LAUNCHER")
    root.geometry("300x200")
    root.overrideredirect(0)


    # ==================== FRAME CONTROL ====================
    frame_control = Frame(root, bg="#505050", width=200, height=20)
    frame_control.pack(side='top', fill=BOTH, expand=0)
    '''Would Be great if it could be specified to only be moved
    when dragging with the Frame above.'''
    grip = Grip(frame_control)

    button_window_exit = Button(frame_control, text="X", width=3, height=1, bg="#FF3333", fg="white", command=lambda: exit())
    button_window_exit.pack(side='right')

    button_window_fullscreen = Button(frame_control, text="^", width=3, height=1, bg="white", fg="black", command=lambda: exit())
    button_window_fullscreen.pack(side='right')

    button_window_down = Button(frame_control, text="_", width=3, height=1, bg="white", fg="black", command=lambda: exit())
    button_window_down.pack(side='right')

    button_window_topalways = Button(frame_control, text="top", width=3, height=1, bg="white", fg="black", command=lambda: exit())
    button_window_topalways.pack(side='right')

    button_window_settings = Button(frame_control, text="Настройки", height=1, bg="white", fg="black", command=lambda: exit())
    button_window_settings.pack(side='right')


    # ==================== FRAME MAIN ====================
    frame_back = Frame(root, bg="grey")
    frame_back.pack_propagate(0)
    frame_back.pack(side='top', fill=BOTH, expand=1)

    root.mainloop()


if __name__ == '__main__':
    main()