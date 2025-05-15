# ---------- Importing libraries ----------
from PySide6.QtWidgets import QMessageBox
import globals
import subprocess

def i_one_init(mode: str):
    globals.ioneInit = 0

    if mode == "lum":
        cmd = [f"{globals.binpath}/spotread.exe", "-u", "-e", "-y", globals.i1yval, "-O"]
    elif mode == "lux":
        cmd = [f"{globals.binpath}/spotread.exe", "-u", "-a", "-O"]
    else:
        print("Error: iOneInit requires a mode of lum or lux")
        globals.srMode = 0
        return 0

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(timeout=10)
        globals.srid = proc.pid
        print("pid:", globals.srid)

        # simulate Tcl string check
        if "Result is" in stdout:
            globals.meterStatus = 1
        else:
            globals.meterStatus = 0

        if globals.meterStatus == 1:
            globals.ioneInit = 1
            print("Photometer initialized correctly.")
            globals.srMode = mode
            return 1
        else:
            print("Error: Photometer failed to initialize.")
            globals.srMode = 0
            return 0

    except Exception as e:
        print("Error:", e)
        return 0

def initIL():
    if globals.LUTmode == 0:
        return

    if globals.meter == "i1DisplayPro":
        globals.i1yval = "n"

        if i_one_init("lum") != 1:
            QMessageBox.critical(
                None,
                "FATAL ERROR",
                "Error initializing i1Display"
            )
            return 0
    else:
        QMessageBox.critical(
            None,
            "Photometer Error",
            "Undefined Photometer type in LRconfig.txt"
        )

    return 1

# ---------- Initialize photometer ----------
def il_init():
    if globals.record == 1:
        QMessageBox.critical(None, "Error", "Data acquisition must be stopped before re-initializing.")
        return

    # Confirm photometer connection
    answer = QMessageBox.question(
        None,
        "Confirm Connection",
        f"Is the {globals.meter} Photometer connected and positioned in the black square?",
        QMessageBox.Yes | QMessageBox.No
    )

    if answer == QMessageBox.Yes:
        globals.ILstatus = 1
        globals.ILval = 0.00
        globals.ILavg = 0.00
        globals.ILcnt = globals.avgN + 2
        globals.ILautoNum = 0

        if initIL() == 0:
            QMessageBox.critical(None, "Meter Error", "ERROR: Meter did not initialize")
            globals.ILstatus = 0
            return

        # Set label colors in the lumMeter panel
        try:
            globals.lumMeter.avg.setStyleSheet(f"color: {globals.fgClr}")
            globals.lumMeter.gmajor.setStyleSheet(f"color: {globals.fgClr}")
            globals.lumMeter.gminor.setStyleSheet(f"color: {globals.fgClr}")
        except AttributeError:
            print("Warning: lumMeter GUI elements not set in globals")

    else:
        return

    globals.ILdataReady = 0
    globals.ILfilt = 0
    globals.lastILavg = 0
