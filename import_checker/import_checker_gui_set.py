#from import_checker import *    # ONLY TO RESOLVE FUNCTIONS AND VARS NAMES HERE
# #################################################
# GUI TREE
# you need only 2 dictionary
# #################################################
# markers
ROOT = "root"
ROOT_METHODS = "ROOT_METHODS"
WM_ATTRIBUTES = "wm_attributes"

# sections in dicts
WGT_TYPE = "WGT_TYPE"
WGT_PARAMETERS = "WGT_PARAMETERS"
PACKER = "PACKER"
PACKER_GRID_CONFIGURE = "PACKER_GRID_CONFIGURE"
PACKER_PARAMETERS = "PACKER_PARAMETERS"
INTERNAL_WGTS = "INTERNAL_WGTS"

# -------------------------------------------------
# 2 - GUI_WGT_TREE_DICT
# -------------------------------------------------
GUI_WGT_TREE_DICT = {
    # all keys must have registered names in GuiFramework!
    "WGT_ID": {  # unique widget name
        WGT_TYPE: "Frame",     # "Frame|Label|Button|..."
        WGT_PARAMETERS: {
            # all parameters will apply individually one by one with TRY-EXCEPT sentence!
            # you may leave inapplicable
            # COMMON
            "text": "привет", "font": ("", 30),
            "fg": None, "bg": "black",
            "width": None, "height": None,
            "bind": None,
            #"image": "image",   # imgObj

            # FOR FRAMES/Label/Root///
            "relief": "raised", # "flat"/"sunken"/"raised"/"groove"/"ridge"
            "borderwidth": 5,   # ширина рамки!

            # FOR BUTTONS
            "activeforeground": None,  # color when pressed state
            "command": "",
        },
        PACKER: "pack",    # "pack|grid|place"
        PACKER_GRID_CONFIGURE: {
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
        PACKER_PARAMETERS: {
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
        INTERNAL_WGTS: {
            # OTHER WIDGETS. just place your internal gui-dict-tree here
        },
    },
}
