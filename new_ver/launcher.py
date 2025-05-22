import sys
import globals
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit, QLabel,
    QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame, QStatusBar
)
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Qt

from window_initializer import initialize
from meter_initializer import il_init
from saver import IL_save
from recorder import IL_rec

def create_button(text, on_click):
    btn = QPushButton(text)
    btn.clicked.connect(on_click)
    return btn

class CalibrationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pacsDisplay Launcher")
        self.setMinimumSize(700, 500)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f7f9fb;
            }
            QPushButton {
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 6px;
                background-color: #0078d4;
                color: white;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                padding: 8px;
                font-family: Consolas, monospace;
                font-size: 13px;
            }
            QLabel#TitleLabel {
                font-size: 20px;
                font-weight: bold;
                color: #333333;
            }
        """)

        title_label = QLabel("Display Calibration Tool")
        title_label.setObjectName("TitleLabel")
        title_label.setAlignment(Qt.AlignCenter)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        self.start_btn = QPushButton("Calibrate")
        self.stop_btn = QPushButton("Stop")
        self.clear_btn = QPushButton("Clear Log")

        self.start_btn.clicked.connect(lambda: self.log("[INFO] Measurement started."))
        self.stop_btn.clicked.connect(lambda: self.log("[INFO] Measurement stopped."))
        self.clear_btn.clicked.connect(lambda: self.log_output.clear())

        self.init_btn = create_button("Initialize", self.handle_initialize)
        self.init_meter_btn = create_button("Init Meter", il_init)
        self.rec_btn = create_button("RECORD", self.handle_record)
        self.save_btn = create_button("Save", IL_save)

        btn_layout_top = QHBoxLayout()
        btn_layout_top.addWidget(self.init_btn)
        btn_layout_top.addWidget(self.init_meter_btn)
        btn_layout_top.addWidget(self.rec_btn)
        btn_layout_top.addWidget(self.save_btn)
        btn_layout_top.addStretch()

        btn_layout_bottom = QHBoxLayout()
        btn_layout_bottom.addWidget(self.start_btn)
        btn_layout_bottom.addWidget(self.stop_btn)
        btn_layout_bottom.addWidget(self.clear_btn)
        btn_layout_bottom.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addSpacing(10)
        layout.addLayout(btn_layout_top)
        layout.addWidget(self.log_output)
        layout.addLayout(btn_layout_bottom)

        self.status = QStatusBar()
        self.status.showMessage("Ready")
        layout.addWidget(self.status)

        self.setLayout(layout)

    def log(self, message):
        self.log_output.append(message)
        self.status.showMessage(message)

    def handle_initialize(self):
        globals.test_window = initialize()
        self.log("[INFO] Window initialized.")

    def handle_record(self):
        IL_rec(globals.test_window, self.rec_btn)
        self.log("[INFO] Recording triggered.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CalibrationApp()
    win.show()
    sys.exit(app.exec())