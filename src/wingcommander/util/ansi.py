CSI_SEQ = "\033["

CLEAR_TO_END = 0
CLEAR_TO_BEG = 1
CLEAR_FULL = 2


def CSI(code, n=''):
    return CSI_SEQ + str(n) + code


def __gen0CSI(code, doc=None):
    def handler():
        return CSI_SEQ + code

    if doc is not None:
        handler.__doc__ = doc

    return handler


def __gen1CSI(code, default=None, doc=None):
    if default is None:
        def handler(n):
            return CSI(code, n)
    else:
        def handler(n=default):
            return CSI(code, n)

    if doc is not None:
        handler.__doc__ = doc

    return handler


def __gen2CSI(code, doc=None):
    def handler(a=1, b=2):
        return CSI_SEQ + str(a) + ';' + str(b) + code

    if doc is not None:
        handler.__doc__ = doc

    return handler


# ANSI Terminal Controls
CUU = __gen1CSI('A', 1, doc="Move the cursor up")
CUD = __gen1CSI('B', 1, doc="Move the cursor down")
CUF = __gen1CSI('C', 1, doc="Move the cursor forward")
CUB = __gen1CSI('D', 1, doc="Move the cursor backward")
CNL = __gen1CSI('E', 1,
                doc="Move the cursor to beginning of line, n lines down")
CPL = __gen1CSI('F', 1, doc="Move the cursor to beginning of line, n lines up")
CHA = __gen1CSI('G', 1, doc="Move the cursor to column n")
CUP = __gen2CSI('H', doc="Move the cursor to the X, Y position specified")
ED = __gen1CSI('J',
               doc="Clears the display, if 0, from cursor to end, " +
               "if 1, from cursor to beginning, if 2, the full display")
EL = __gen1CSI('K',
               doc="Clears the current line, if 0, from cursor to end, " +
               "if 1, from cursor to beginning, if 2, the full line")
SU = __gen1CSI('S', 1, doc="Scroll page up")
SD = __gen1CSI('T', 1, doc="Scroll page down")
HVP = __gen2CSI('f', doc="Move the cursor to the X, Y position specified")
SGR = __gen1CSI('m', doc="Graphic Rendition (text colors and effects)")
SCP = __gen0CSI('s', doc="Save cursor position")
RCP = __gen0CSI('u', doc="Restores cursor position")

# SGR fg colors
BLACK = SGR(0 + 30)
RED = SGR(1 + 30)
GREEN = SGR(2 + 30)
YELLOW = SGR(3 + 30)
BLUE = SGR(4 + 30)
MAGENTA = SGR(5 + 30)
CYAN = SGR(6 + 30)
WHITE = SGR(7 + 30)

# SGR bg colors
BLACK_BG = SGR(0 + 40)
RED_BG = SGR(1 + 40)
GREEN_BG = SGR(2 + 40)
YELLOW_BG = SGR(3 + 40)
BLUE_BG = SGR(4 + 40)
MAGENTA_BG = SGR(5 + 40)
CYAN_BG = SGR(6 + 40)
WHITE_BG = SGR(7 + 40)
