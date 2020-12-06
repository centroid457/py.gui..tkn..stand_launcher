"""
GUI_TREE_DICT = {
    # all keys must have registered names in GuiFramework!
    _ROOT_CONFIGURE: {     # KEEP IT ONLY IN FIRST KEY LEVEL!
        # use only none dictionary parameters! only specific methods!
        # for usual dict-like parameters use first WGT_ID in first level in dictionary
        "title": "title",  # root.title("title")
        "geometry": "250x150+0+100", #"root.geometry("250x150+0+100")" #("WINXxWINY+ShiftX+ShiftY")
        "resizable": None, # root.resizable(width=False, height=False)	# заблокировать возможность изменения размеров границ! В том числе на весь экран!!!
        "maxsize": None,  # root.maxsize(300, 300)
        "minsize": None,  # root.minsize(300, 300)
        "overrideredirect": True,   # root.overrideredirect(True)   =True/False
        "state": 'normal',   # root.state('zoomed')     normal/zoomed/iconic/withdrawn
        "iconbitmap": r'ERROR.ico', # root.iconbitmap('ERROR.ico')    =ONLY FILENAME! NO fileobject
        "wm_attributes": {
            "-topmost": 0,  # root.wm_attributes("-topmost", True)
            "-disabled": 0,  # root.wm_attributes("-disabled", True)
            "-fullscreen": 0,  # root.wm_attributes("-fullscreen", True)
            "-transparentcolor": 0,  # root.wm_attributes("-transparentcolor", "white")
        },
    },
    "WGT_ID": {  # unique widget name
        _WGT_TYPE: "Frame",     # "Frame|Label|Button|..."
        _WGT_PARAMETERS: {
            # all parameters will apply individually one by one with TRY-EXCEPT sentence!
            # you may leave inapplicable
            # COMMON
            "text": None, "font": ("", 30),
            "fg": None, "bg": None,
            "width": None, "height": None,
            "bind": None,
            "image": "image",   # imgObj

            # FOR FRAMES
            "relief": "raised",
            "borderwidth": 5,

            # FOR BUTTONS
            "activeforeground": None,  # color when pressed state
            "command": "",
        },
        _PACKER: "pack",    # "pack|grid|place"
        _PACKER_GRID_CONFIGURE: {
            "columnconfigure": {
                "COLUMNS": {"column": [0, ], "minsize": 250, "pad": 0, },
                "minsize": 250,  # minimal size in letters
            },
            "rowconfigure": {
                "ROWS": {"row": [0, ], "minsize": 250, "pad": 0, },
                "minsize": 1,
            },
            # COMMON =-minsize, -pad, -uniform, or -weight
            "pad": 3,    # external pads
            "weight": 1,    # expansion ratio
        },
        _PACKER_PARAMETERS: {
            # delete yourself inapplicable parameters!
            # COMMON
            "padx": 0, "pady": 0,       # external pads
            "ipadx": 0, "ipady": 0,     # internal pads
            # FOR PACK
            "side": "left",    # "left|right|top|bottom"
            "fill": "both",    # 'x', 'y', 'both', 'none'.
            "expand": True,     # True / False

            # FOR GRID [-column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky]
            "row": 0, "column": 1,
            "rowspan": 4, "columnspan": 4,  # expansion additional positions
            "sticky": "w",      #"ewsn"
        },
        _INTERNAL_WGTS: {
            # OTHER WIDGETS. just place your internal gui-dict-tree here
        },
    },
}
"""

# #################################################
# GUI TREE
# #################################################
# markers
_ROOT_NAME = "root"

# sections in dict
_ROOT_CONFIGURE = "ROOT_CONFIGURE"
_WGT_TYPE = "WGT_TYPE"
_WGT_PARAMETERS = "WGT_PARAMETERS"
_PACKER = "PACKER"
_PACKER_GRID_CONFIGURE = "PACKER_GRID_CONFIGURE"
_PACKER_PARAMETERS = "PACKER_PARAMETERS"
_INTERNAL_WGTS = "INTERNAL_WGTS"

# gui dict
GUI_TREE_DICT = {
    # all keys must have registered names in GuiFramework!
    _ROOT_CONFIGURE: {     # KEEP IT ONLY IN FIRST KEY LEVEL!
        # use only none dictionary parameters! only specific methods!
        # for usual dict-like parameters use first WGT_ID in first level in dictionary
        "title": "title",  # root.title("title")
        "geometry": "250x150+0+100", #"root.geometry("250x150+0+100")" #("WINXxWINY+ShiftX+ShiftY")
        "resizable": None, # root.resizable(width=False, height=False)	# заблокировать возможность изменения размеров границ! В том числе на весь экран!!!
        "maxsize": None,  # root.maxsize(300, 300)
        "minsize": None,  # root.minsize(300, 300)
        "overrideredirect": True,   # root.overrideredirect(True)   =True/False
        "state": 'normal',   # root.state('zoomed')     normal/zoomed/iconic/withdrawn
        "iconbitmap": r'ERROR.ico', # root.iconbitmap('ERROR.ico')    =ONLY FILENAME! NO fileobject
        "wm_attributes": {
            "-topmost": 0,  # root.wm_attributes("-topmost", True)
            "-disabled": 0,  # root.wm_attributes("-disabled", True)
            "-fullscreen": 0,  # root.wm_attributes("-fullscreen", True)
            "-transparentcolor": 0,  # root.wm_attributes("-transparentcolor", "white")
        },
    },
    "WGT_ID": {  # unique widget name
        _WGT_TYPE: "Frame",     # "Frame|Label|Button|..."
        _WGT_PARAMETERS: {
            # all parameters will apply individually one by one with TRY-EXCEPT sentence!
            # you may leave inapplicable
            # COMMON
            "text": None, "font": ("", 30),
            "fg": None, "bg": None,
            "width": None, "height": None,
            "bind": None,
            "image": "image",   # imgObj

            # FOR FRAMES
            "relief": "raised",
            "borderwidth": 5,

            # FOR BUTTONS
            "activeforeground": None,  # color when pressed state
            "command": "",
        },
        _PACKER: "pack",    # "pack|grid|place"
        _PACKER_GRID_CONFIGURE: {
            "columnconfigure": {
                "COLUMNS": {"column": [0, ], "minsize": 250, "pad": 0, },
                "minsize": 250,  # minimal size in letters
            },
            "rowconfigure": {
                "ROWS": {"row": [0, ], "minsize": 250, "pad": 0, },
                "minsize": 1,
            },
            # COMMON =-minsize, -pad, -uniform, or -weight
            "pad": 3,    # external pads
            "weight": 1,    # expansion ratio
        },
        _PACKER_PARAMETERS: {
            # delete yourself inapplicable parameters!
            # COMMON
            "padx": 0, "pady": 0,       # external pads
            "ipadx": 0, "ipady": 0,     # internal pads
            # FOR PACK
            "side": "left",    # "left|right|top|bottom"
            "fill": "both",    # 'x', 'y', 'both', 'none'.
            "expand": True,     # True / False

            # FOR GRID [-column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky]
            "row": 0, "column": 1,
            "rowspan": 4, "columnspan": 4,  # expansion additional positions
            "sticky": "w",      #"ewsn"
        },
        _INTERNAL_WGTS: {
            # OTHER WIDGETS. just place your internal gui-dict-tree here
        },
    },
}
