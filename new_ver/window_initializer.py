from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt, QRect
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

# ---------- Custom Measurement Window ----------
class MeasurementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Measurement Window")
        self.showFullScreen()
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw white outline circle in center
        size = min(self.width(), self.height()) // 3
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2

        pen = QPen(Qt.white, 6)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QRect(x, y, size, size))

        # Draw top-left gray info box
        box_width = 200
        box_height = 100
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(200, 200, 200))
        painter.drawRect(20, 20, box_width, box_height)

        # Draw text inside info box
        painter.setPen(QPen(Qt.black))
        painter.drawText(QRect(25, 25, box_width - 10, box_height - 10),
                         Qt.AlignLeft | Qt.AlignTop,
                         "Info Box:\nGrey Level = {}\nCHRv = ???\nCHRu = ???".format(globals.greyR_display))

    def mousePressEvent(self, event):
        msg = QMessageBox(self)
        msg.setWindowTitle("Exit Confirmation")
        msg.setText("Do you want to close the window?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setStyleSheet("font-size: 14px;")
        msg.move(self.width() - 350, 50)
        reply = msg.exec()
        if reply == QMessageBox.Yes:
            self.close()

# ---------- Initialize ----------
def initialize():
    globals.greyR = 0
    globals.greyR_display = f"{max(globals.greyR + globals.greyR_offset, 0):3d}"

    color = color_rgb(-5)
    w = MeasurementWindow()
    w.setStyleSheet(f"background-color: {color};")

    globals.start = 1
    w.show()
    return w
