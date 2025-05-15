# ---------- Importing libraries ----------
from PySide6.QtWidgets import QWidget
import globals

# ---------- Getting rgb color based on grey level ----------
def color_rgb(grey):
    grey = max(0, min(grey, 255))

    raw = globals.phase.get(globals.LUTphase, "0 0 0") if globals.LUTmode and grey < 255 else "0 0 0"

    if isinstance(raw, str):
        shift = [int(s) for s in raw.strip().split()]
    else:
        shift = list(raw)

    r, g, b = [max(0, min(grey + int(s), 255)) for s in shift]


    color = f"#{r:02x}{g:02x}{b:02x}"
    globals.lastRGB = color
    return color

# ---------- Initialize with GUI ----------
def initialize():

    w = QWidget()
    w.resize(400, 400)
    w.setMinimumSize(300, 300)
    w.setWindowTitle("Measurement Window")

    globals.greyR = globals.greyR_init
    globals.greyR_display = f"{max(globals.greyR + globals.greyR_offset, 0):3d}"

    color = color_rgb(-5)
    w.setStyleSheet(f"background-color: {color};")

    w.show()

    globals.start = 1

    return w
