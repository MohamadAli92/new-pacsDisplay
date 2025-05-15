import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QLabel
)

from lumResponse import initialize, il_init, IL_rec

test_window = None  # global-level reference to the .lum window

# List to keep window references
opened_windows = []

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("pacsDisplay Launcher")
window.setMinimumWidth(300)

layout = QVBoxLayout()
layout.addWidget(QLabel("Launcher Panel"))

# Button 1: Initialize
def handle_initialize():
    global test_window
    test_window = initialize()

btn_init = QPushButton("Initialize")
btn_init.clicked.connect(lambda: handle_initialize())
layout.addWidget(btn_init)

# Button 2: Init Meter
btn_il = QPushButton("Init Meter")
btn_il.clicked.connect(lambda: il_init())
layout.addWidget(btn_il)

from PySide6.QtWidgets import QHBoxLayout

# Button 3: Init record

btn_rec = QPushButton("RECORD")
btn_rec.clicked.connect(lambda: IL_rec(test_window, btn_rec))
layout.addWidget(btn_rec)

# Button 4: Empty
btn4 = QPushButton("Reserved 2")
btn4.clicked.connect(lambda: None)
layout.addWidget(btn4)

window.setLayout(layout)
window.show()
sys.exit(app.exec())
