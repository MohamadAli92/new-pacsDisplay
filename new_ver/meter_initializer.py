# ---------- Importing libraries ----------
from PySide6.QtWidgets import QMessageBox
import globals
import subprocess

def il_init():
    if globals.record == 1:
        QMessageBox.critical(None, "Error", "Data acquisition must be stopped before re-initializing.")
        return

    answer = QMessageBox.question(
        None,
        "Confirm Connection",
        f"Is the {globals.meter} Photometer connected and positioned in the black square?",
        QMessageBox.Yes | QMessageBox.No
    )

    if answer != QMessageBox.Yes:
        return

    success, message = il_init_logic()

    if not success:
        QMessageBox.critical(None, "Meter Error", message)
        return

    try:
        globals.lumMeter.avg.setStyleSheet("color: #00ff00")
        globals.lumMeter.gmajor.setStyleSheet("color: #00ff00")
        globals.lumMeter.gminor.setStyleSheet("color: #00ff00")
    except AttributeError:
        print("Warning: lumMeter GUI elements not set")

    QMessageBox.information(None, "Init Meter", message)

def i_one_init(mode: str) -> tuple[bool, str]:
    if mode == "lum":
        cmd = [f"{globals.binpath}/spotread.exe", "-u", "-e", "-y", globals.i1yval, "-O"]
    elif mode == "lux":
        cmd = [f"{globals.binpath}/spotread.exe", "-u", "-a", "-O"]
    else:
        globals.srMode = 0
        return False, "Invalid mode passed to i_one_init (must be 'lum' or 'lux')"

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, _ = proc.communicate(timeout=10)
        globals.srid = proc.pid

        if "Result is" in stdout:
            globals.meterStatus = 1
            globals.srMode = mode
            return True, "Photometer initialized successfully."
        else:
            globals.meterStatus = 0
            globals.srMode = 0
            return False, "Photometer failed to initialize."

    except Exception as e:
        return False, f"Exception while running spotread: {e}"

def initIL() -> tuple[bool, str]:
    if globals.LUTmode == 0:
        return True, "LUTmode inactive (demo mode), skipping init."

    if globals.meter != "i1DisplayPro":
        return False, "Undefined Photometer type in LRconfig.txt"

    globals.i1yval = "n"
    return i_one_init("lum")

# ---------- Initialize photometer ----------
def il_init_logic() -> tuple[bool, str]:
    globals.ILstatus = 1
    globals.ILval = 0.0
    globals.ILavg = 0.0
    globals.ILcnt = globals.avgN + 2
    globals.ILautoNum = 0

    success, message = initIL()
    if not success:
        globals.ILstatus = 0
        return False, message

    globals.ILfilt = 0
    globals.lastILavg = 0
    return True, "Meter initialized and ready."
