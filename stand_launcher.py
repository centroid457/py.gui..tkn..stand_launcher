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

    frame_control = Frame(root, bg="#505050", width=200, height=20)
    frame_control.pack(side='top', fill=BOTH, expand=0)
    '''Would Be great if it could be specified to only be moved
    when dragging with the Frame above.'''
    grip = Grip(frame_control)

    button_exit = Button(frame_control, text="X", bg="#FF6666", fg="white", command=lambda: exit())
    button_exit.pack(side='right')


    frame_back = Frame(root, bg="grey")
    frame_back.pack_propagate(0)
    frame_back.pack(side='top', fill=BOTH, expand=1)

    root.mainloop()

main()
