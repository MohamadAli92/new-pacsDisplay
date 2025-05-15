import globals
from pathlib import Path
from window_initializer import initialize, color_rgb
import subprocess

from PySide6.QtWidgets import (
    QApplication, QMessageBox, QFileDialog
)

from PySide6.QtCore import QEventLoop, QTimer


def delay(ms: int):
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec()


def ILoutlierTest():
    if globals.greyR == 0 and globals.LUTphase == 0:
        globals.relChange = 0
        globals.absChange = 0
        mabsChange = 0
    else:
        globals.absChange = globals.ILavg - globals.lastILavg
        mabsChange = abs(globals.absChange)
        avg = (globals.ILavg + globals.lastILavg) / 2.0
        globals.relChange = globals.absChange / avg if avg != 0 else 0

    # Check if inside acceptable limits
    if (
            mabsChange <= globals.ILlimit_abs or
            (globals.ILlimit_minus <= globals.relChange <= globals.ILlimit_plus)
    ):
        if globals.outlierTestCount != 0:
            globals.outlierResolve += 1
            globals.outlierTestCount = 0
        return 0  # no outlier
    else:
        globals.outlierTestCount += 1

        if globals.outlierTestCount == 1:
            globals.outlierTotal += 1
            marker = "**"
        else:
            marker = "*"

        textmsg = f"  {int(globals.greyR_display):4d}   {globals.LUTphase_display}"
        textmsg += f"     {globals.ILavg:7.3f}  {globals.lastRGB}   {globals.lastILavg:7.3f}"
        textmsg += f"    {globals.relChange:1.4f} {globals.absChange:1.4f} {marker}"

        print(textmsg)
        if globals.log and hasattr(globals.log, "write"):
            globals.log.write(textmsg + "\n")

        if globals.outlierTestCount < globals.outlierNum:
            return 1  # retry

        # Final check with tolerance limits
        tolerance_abs = globals.ILlimit_abs * globals.ILtolerance
        tolerance_plus = globals.ILlimit_plus * globals.ILtolerance
        tolerance_minus = globals.ILlimit_minus * globals.ILtolerance

        if (
                mabsChange <= tolerance_abs or
                (tolerance_minus <= globals.relChange <= tolerance_plus)
        ):
            globals.outlierAccept += 1
            msg = "WARNING: Too many outliers. Outlier value accepted by tolerance limit."
            print(msg)
            if globals.log and hasattr(globals.log, "write"):
                globals.log.write(msg + "\n")
            return 0  # accept outlier
        else:
            globals.pause_flag = 1
            detail = (
                "Persistent outlier detected.\n\nCurrent values:\n"
                f"  ILavg     = {globals.ILavg:.3f}\n"
                f"  lastRGB   = {globals.lastRGB}\n"
                f"  lastILavg = {globals.lastILavg:.3f}\n"
                f"  relChange = {globals.relChange:.4f}\n"
                f"  absChange = {globals.absChange:.4f}\n\n"
                "Do you wish to accept the outlier value?"
            )
            answer = QMessageBox.question(
                None, "Outlier Detected", detail,
                QMessageBox.Yes | QMessageBox.No
            )

            if answer == QMessageBox.Yes:
                globals.outlierAccept += 1
                msg = "WARNING: Too many outliers. Outlier value accepted by user."
                print(msg)
                if globals.log and hasattr(globals.log, "write"):
                    globals.log.write(msg + "\n")
                globals.pause_flag = 0
                return 0
            else:
                globals.error = 1
                msg = "ERROR: Too many outliers. Measurement aborted by user."
                print(msg)
                if globals.log and hasattr(globals.log, "write"):
                    globals.log.write(msg + "\n")
                globals.pause_flag = 0
                return 1


def iOneRead():
    if globals.srMode == "lum":
        sropt = "-e"
    elif globals.srMode == "lux":
        sropt = "-a"
    else:
        sropt = ""

    cmd = [
        f"{globals.binpath}/spotread.exe",
        "-u", sropt,
        "-y", globals.i1yval,
        "-O"
    ]

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        globals.srid = proc.pid
        stdout, stderr = proc.communicate(timeout=10)
        globals.srout = stdout.strip()
        globals.iOneDone = True
        return 1

    except Exception as e:
        print("Error:", e)
        return 0


def iOneCall():
    for i in range(globals.avgN):
        if iOneRead() != 1:
            QMessageBox.critical(
                None,
                "FATAL ERROR",
                "Error: i1Display read utility"
            )
            return 0
    return 1


def Next_greyR(w, change):
    if globals.start == 0:
        globals.test_window = initialize()

    if globals.greyR >= 0:
        globals.greyR += change
    else:
        globals.greyR += 1

    if globals.greyR > 255:
        globals.greyR = 255

    globals.greyR_display = f"{max(globals.greyR + globals.greyR_offset, 0):3d}"
    if int(globals.greyR_display) > 255 + globals.greyR_offset:
        globals.greyR_display = str(255 + globals.greyR_offset)

    try:
        color = color_rgb(globals.greyR)
        w.setStyleSheet(f"background-color: {color};")
    except Exception as e:
        print("Next_greyR error:", e)


def IL_auto(w):
    globals.error = 0

    # reset outlier indicator (placeholder for GUI logic)
    # try:
    #     globals.lumMeter.outlier.setStyleSheet(f"color: {globals.bgClr}")
    # except AttributeError:
    #     pass  # will hook GUI later

    # LUTmode-specific setup
    if globals.LUTmode != 0:
        base_path = Path.cwd()
        input_path = ""

        if globals.LUTmode == 1786:
            input_path = base_path / "1786phase.txt"
        elif globals.LUTmode == 766:
            input_path = base_path / "766phase.txt"
        elif globals.LUTmode == 256:
            input_path = base_path / "256phase.txt"
        elif globals.LUTmode == 52:
            input_path = base_path / "256phase.txt"
            globals.dGrey = 5
        elif globals.LUTmode == 18:
            input_path = base_path / "256phase.txt"
            globals.dGrey = 15
        elif globals.LUTmode == 16:
            input_path = base_path / "16phase.txt"
            globals.dGrey = 16
        elif globals.LUTmode == 1:
            answer = QMessageBox.question(
                None,
                "Phase File",
                globals.msgOther,
                QMessageBox.Yes | QMessageBox.No
            )
            if answer == QMessageBox.Yes:
                path = QFileDialog.getOpenFileName(None, "Select PHASE file")[0]
                if not path:
                    return
                input_path = Path(path)
            else:
                return

        try:
            with open(input_path, "r") as f:
                f.readline()  # skip header
                f.readline()
                globals.numPhases = int(f.readline().strip())
                for i in range(globals.numPhases):
                    line = f.readline()
                    if not line:
                        QMessageBox.critical(None, "Error", "Incorrect number of lines in phase file")
                        return
                    globals.phase[i] = line.strip()
                tail = f.readline()
                if tail:
                    QMessageBox.critical(None, "Error", "Extra lines in phase file")
                    return
        except Exception as e:
            QMessageBox.critical(None, "File Error", f"Cannot open {input_path}\n{e}")
            return

    if globals.start == 0:
        globals.test_window = initialize()

    # # set initial grey level
    # globals.greyR = globals.greyR_init
    # globals.greyR_display = f"{max(globals.greyR + globals.greyR_offset, 0):3d}"

    # update canvas rectangle color
    # try:
    #     canvas = w.findChild(type(w), "canvas")  # placeholder: replace with actual ref
    #     color = ColorRGB(globals.greyR)
    #     canvas.setStyleSheet(f"background-color: {color}")  # placeholder for actual item update
    # except Exception:
    #     pass

    # open log file
    try:
        globals.log = open(globals.logfile, "w")
    except Exception as e:
        QMessageBox.critical(None, "Log Error", f"Cannot open logfile: {e}")
        return

    from datetime import datetime
    timestamp = datetime.now().strftime("%D %T")

    header = f"# Photometer filter log - {timestamp}"
    globals.log.write(header + "\n")
    print(header)

    subheader = "# Major Minor   ILavg   lastRGB  lastILavg  relChange  absChange"
    globals.log.write(subheader + "\n")
    print(subheader)

    if globals.ILstatus != 0:
        globals.ILautoNum = 0
        globals.lastILavg = 0
        globals.outlierTestCount = 0
        globals.outlierTotal = 0
        globals.outlierResolve = 0
        globals.outlierAccept = 0
        globals.relChange = 0
        globals.absChange = 0

        if globals.LUTmode != 0:
            while globals.greyR < 256:
                for globals.LUTphase in range(globals.numPhases):
                    if globals.greyR >= 0:
                        Next_greyR(w, +0)

                    if globals.greyR <= 0 and globals.LUTphase == 0:
                        delay(1000)
                        if globals.greyR == 0 and globals.LUTmode not in (16, 18, 52):
                            globals.ILfilt = 1

                    globals.ILcnt = 1 - globals.iLdelay
                    globals.ILavg = 0.0
                    globals.CHRuAvg = 0.0
                    globals.CHRvAvg = 0.0

                    delay(100)  # let display stabilize
                    iOneCall()  # blocking until valid reading is ready

                    if globals.error != 0 or globals.record == 0:
                        break

                    # Store luminance
                    globals.autoLumVal[globals.ILautoNum] = globals.ILavg
                    globals.autoLumRGB[globals.ILautoNum] = globals.lastRGB
                    globals.ILavg_display = f"{globals.ILavg:.3f}"

                    # Store chrominance
                    globals.autoCHRuVal[globals.ILautoNum] = globals.CHRuAvg
                    globals.autoCHRvVal[globals.ILautoNum] = globals.CHRvAvg

                    # Update display strings
                    globals.greyR_display = f"{max(globals.greyR + globals.greyR_offset, 0):3d}"
                    globals.LUTphase_display = str(globals.LUTphase + 1)

                    # Check for outlier
                    if globals.ILfilt != 0 and ILoutlierTest() != 0:
                        if globals.error != 0:
                            break
                        try:
                            globals.lumMeter.outlier.setStyleSheet(f"color: {globals.fgClr}")
                        except AttributeError:
                            pass
                        delay(globals.outlierpause)
                        globals.ILautoNum -= 1
                        globals.LUTphase -= 1
                        continue
                    else:
                        try:
                            globals.lumMeter.outlier.setStyleSheet(f"color: {globals.bgClr}")
                        except AttributeError:
                            pass

                        if globals.ILfilt != 0:
                            globals.lastILavg = globals.ILavg

                        textmsg = f"  {int(globals.greyR_display):4d}   {globals.LUTphase_display}"
                        textmsg += f"     {globals.ILavg:7.3f}  {globals.lastRGB}   {globals.lastILavg:7.3f}"
                        if globals.ILfilt != 0:
                            textmsg += f"    {globals.relChange:1.4f} {globals.absChange:1.4f}"

                        print(textmsg)
                        globals.log.write(textmsg + "\n")

                    if globals.greyR == 255 or globals.greyR < 0:
                        break

                if globals.error != 0 or globals.record == 0:
                    break

                globals.LUTphase = 0
                if globals.greyR == 255:
                    break

                Next_greyR(w, globals.dGrey)
                QApplication.processEvents()

    else:  # demo mode
        globals.avgN = 2
        globals.iLdelay = 2
        globals.dGrey = 15
        globals.numPhases = 1

        while globals.greyR < 256:
            globals.ILavg = float(globals.greyR) if globals.greyR >= 0 else 0.0
            globals.CHRuAvg = 0.3127
            globals.CHRvAvg = 0.3290

            delay(1000)
            globals.ILautoNum += 1

            globals.autoLumVal[globals.ILautoNum] = globals.ILavg
            globals.autoLumRGB[globals.ILautoNum] = globals.lastRGB
            globals.ILavg_display = f"{globals.ILavg:.3f}"
            globals.autoCHRuVal[globals.ILautoNum] = globals.CHRuAvg
            globals.autoCHRvVal[globals.ILautoNum] = globals.CHRvAvg

            globals.greyR_display = f"{max(globals.greyR + globals.greyR_offset, 0):3d}"

            if globals.greyR == 255 or globals.record == 0:
                break

            Next_greyR(w, globals.dGrey)

        globals.dGrey = 1  # reset

    # After loop – wrap up
    globals.ILfilt = 0

    try:
        color = color_rgb(0)
        canvas = w.findChild(type(w), "canvas")  # placeholder
        canvas.setStyleSheet(f"background-color: {color}")
    except Exception:
        pass

    globals.greyR = 0
    globals.greyR_display = f"{max(globals.greyR + globals.greyR_offset, 0):3d}"

    if globals.error != 0:
        QMessageBox.critical(None, "Error", "ERROR - See log file for details.")
        return
    else:
        print("Measurement complete.")

    try:
        globals.log.close()
    except Exception:
        pass
    globals.log = None

    if globals.record == 0:
        return

    globals.ILdataReady = 1

    textmsg = (
        "Luminance Measurement Complete\n\n"
        f"Number of outliers = {globals.outlierTotal}\n"
        f"Resolved outliers  = {globals.outlierResolve}\n"
        f"Accepted outliers  = {globals.outlierAccept}\n\n"
        "SAVE RESULTS BEFORE CHANGING SETTINGS\n\n"
        "Would you like to view the log file?"
    )

    answer = QMessageBox.question(
        None, "View Log File?", textmsg,
        QMessageBox.Yes | QMessageBox.No
    )

    if answer == QMessageBox.Yes:
        try:
            subprocess.Popen(["notepad", globals.logfile])
        except Exception as e:
            QMessageBox.warning(
                None, "WARNING",
                f"Error opening logfile with notepad\n{e}"
            )


def IL_rec(w, btn_rec):
    if globals.ILstatus == 0:
        QMessageBox.critical(None, "Error", "Meter has not been initialized.")
        return

    if globals.record == 0:
        textmsg = (
            "Beginning luminance measurement.\n\n"
            "Please check the following:\n\n"
            "1 - Assert LINEAR LUT (1786 or 766 Mode)\n"
            "    Assert DICOM LUT (256, 52, 18, 16x2 QC Mode)\n\n"
            "2 - Ambient lighting should be minimized\n\n"
            "3 - Turn off screensavers (set to \"None\")\n"
            "    Turn off power-saving (set to \"Never\")\n\n"
            "Start measurement?"
        )

        answer = QMessageBox.question(
            None,
            "Start Measurement",
            textmsg,
            QMessageBox.Yes | QMessageBox.No
        )

        if answer == QMessageBox.Yes:
            globals.record = 1
            btn_rec.setText("STOP")
            IL_auto(w)
        else:
            return

    else:
        answer = QMessageBox.question(
            None,
            "Cancel Operation",
            "Do you wish to cancel the current operation?",
            QMessageBox.Yes | QMessageBox.No
        )

        if answer == QMessageBox.Yes:
            globals.record = 0
            textmsg = "Measurement aborted by user."
            print(textmsg)
            if globals.log and hasattr(globals.log, "write"):
                globals.log.write(textmsg + "\n")
        else:
            return

    globals.record = 0

    try:
        globals.rec_bar.auto.setText("RECORD")
    except AttributeError:
        print("Warning: rec_bar.auto button not assigned in globals.")
