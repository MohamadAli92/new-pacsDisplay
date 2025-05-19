import sys
import globals
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QLabel
)

from window_initializer import initialize
from meter_initializer import il_init
from saver import IL_save
from recorder import IL_rec

def create_button(text, on_click):
    btn = QPushButton(text)
    btn.clicked.connect(on_click)
    return btn

def handle_initialize():
    globals.test_window = initialize()

def handle_record():
    IL_rec(globals.test_window, btn_rec)

# Init app and window
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("pacsDisplay Launcher")
window.setMinimumWidth(300)

layout = QVBoxLayout()
layout.addWidget(QLabel("Launcher Panel"))

# Add buttons
layout.addWidget(create_button("Initialize", handle_initialize))
layout.addWidget(create_button("Init Meter", il_init))

btn_rec = create_button("RECORD", handle_record)
layout.addWidget(btn_rec)

layout.addWidget(create_button("Save", IL_save))

window.setLayout(layout)
window.show()
sys.exit(app.exec())
