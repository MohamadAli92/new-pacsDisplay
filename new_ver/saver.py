from PySide6.QtWidgets import QMessageBox, QFileDialog
import globals
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import globals

def plotUlr(filename: str):
    if globals.LUTmode in {16, 18, 52, 11}:
        print(f"[plotUlr] Skipped: LUTmode={globals.LUTmode} handled by evalQClr")
        return

    try:
        lines = Path(filename).read_text(encoding="utf-8").splitlines()
    except Exception as e:
        print(f"[plotUlr] Error reading file: {e}")
        return

    data_lines = [line for line in lines if not line.strip().startswith("#")]
    if not data_lines:
        print("[plotUlr] No data lines found in file.")
        return

    from io import StringIO
    df = pd.read_csv(StringIO("\n".join(data_lines)), delim_whitespace=True, header=None)

    if df.shape[1] < 6:
        print("[plotUlr] Unexpected file format. Need at least 6 columns.")
        return

    # ----------------- Plot 1: Luminance -----------------
    plt.figure()
    plt.plot(df[0], df[1], label="Luminance", color="blue")
    plt.yscale("log")
    plt.xlabel("Palette Index")
    plt.ylabel("Luminance (cd/m²)")
    plt.title("Luminance vs. Palette Index")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("uLR-PlotULR.png", dpi=150)
    plt.show()

    # ----------------- Plot 2: dL/L by Phase -----------------
    plt.figure()
    for phase in range(1, 8):
        subset = df[df[4] == phase]
        if not subset.empty:
            plt.plot(subset[3], subset[5], label=f"Phase {phase}")

    plt.xlabel("Major Palette Index")
    plt.ylabel("dL/L")
    plt.title("Relative Luminance Change (dL/L)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("uLR-Plot-dL_L.png", dpi=150)
    plt.show()

def build_filename():
    name = "_".join("Monitoring")
    prefix = "cLR" if globals.LUTmode in {256, 52, 18, 16} else "uLR"
    return f"{prefix}_{name}.txt"

def format_measurement(i, major, minor, dLL):
    return (
        f"{i:4d}  {globals.autoLumVal[i]:12.7f}  {globals.autoLumRGB[i]}"
        f"  {major:3d} {minor}"
        f"  {dLL:1.4f}"
        f"  {globals.autoCHRuVal[i]:10.7f}  {globals.autoCHRvVal[i]:10.7f}"
    )

def save_luminance_data(filename: str):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"#  {globals.title} - {datetime.now().strftime('%m/%d/%y %H:%M:%S')}\n")
            f.write(f"#  Display ID: {globals.DisplayName}\n")
            f.write(f"#  iLdelay={globals.iLdelay}  avgN={globals.avgN}  "
                    f"ILlimit_plus={globals.ILlimit_plus} ILlimit_minus={globals.ILlimit_minus}  "
                    f"Meter={globals.meter} LUTmode={globals.LUTmode}\n")

            # initial stabilization (first 3 entries)
            for i in range(1, 4):
                f.write(f"#  {globals.autoLumVal[i]:.6f}  {globals.autoLumRGB[i]}\n")

            major, minor = 1, 1
            dLL = {4: 0.0}

            # first real measurement (i = 4)
            f.write(format_measurement(4, major, minor, dLL[4]) + "\n")
            minor += 1

            for i in range(5, globals.ILautoNum + 1):
                if minor > globals.numPhases:
                    minor = 1
                    major += 1

                j = i - 1
                prev = globals.autoLumVal[j]
                curr = globals.autoLumVal[i]
                dLL[i] = (curr - prev) / ((curr + prev) / 2.0) if (curr + prev) != 0 else 0
                f.write(format_measurement(i - 3, major, minor, dLL[i]) + "\n")
                minor += 1
    except Exception as e:
        raise RuntimeError(f"Error saving data: {e}")

def IL_save():
    if globals.ILstatus != 1:
        QMessageBox.critical(None, "Error", "Photometer I/O channel not initialized, INIT-IL")
        return

    globals.ILdataReady = 1

    if globals.ILdataReady != 1:
        QMessageBox.critical(None, "Error", "Luminance measurements have not been completed.")
        return

    suggested_file = build_filename()
    path, _ = QFileDialog.getSaveFileName(
        None,
        "SELECT DATA SAVE DIRECTORY",
        str("kk"),
        "Text Files (*.txt);;All Files (*)",
        selectedFilter="Text Files (*.txt)"
    )

    if path:
        try:
            save_luminance_data(path)
        except RuntimeError as e:
            QMessageBox.critical(None, "Save Error", str(e))
            return

        # ask for plot
        msg = (
            "Do you wish to analyze the QC (256, 52, 18, or 16x2) saved data?"
            if globals.LUTmode in {256, 52, 18, 16}
            else "Do you wish to see plots of the luminance and dL/L values?"
        )

        answer = QMessageBox.question(None, "Plot?", msg, QMessageBox.Yes | QMessageBox.No)
        if answer == QMessageBox.Yes:
            plotUlr(path)
