import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
from pathlib import Path

# Base path is the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent
BIN_DIR = BASE_DIR / "pacsDisplay-BIN"

# Mapping of buttons to folder and executable
PROGRAMS = {
    "EDIDprofile": "EDIDprofile.exe",
    "iQC": "iQC.exe",
    "QC-check": "QC-check.exe",
    "LutGenerate": "LutGenerate.exe",
    "lumResponse": "lumResponse.exe",
    "uLRstats": "uLRstats.exe",
    "ambtest": "ambtest.exe",
    "gtest": "gtest.exe"
}

def launch_program(folder: str, exe: str):
    exe_path = BIN_DIR / folder / exe
    if not exe_path.exists():
        messagebox.showerror("Error", f"Executable not found:\n{exe_path}")
        return
    try:
        subprocess.Popen([str(exe_path)], cwd=exe_path.parent)
    except Exception as e:
        messagebox.showerror("Execution Error", str(e))

# Create GUI
root = tk.Tk()
root.title("pacsDisplay Launcher")
root.resizable(True, True)
root.configure(bg="#f4f4f4")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", background="#f4f4f4", font=("Segoe UI", 12, "bold"))

container = ttk.Frame(root, padding=20)
container.pack(fill="both", expand=True)

title_label = ttk.Label(container, text="Select a Tool to Launch")
title_label.pack(pady=(0, 15))

for name, exe in PROGRAMS.items():
    btn = ttk.Button(
        container,
        text=name,
        command=lambda n=name, e=exe: launch_program(n, e)
    )
    btn.pack(pady=6, fill="x")

root.mainloop()
