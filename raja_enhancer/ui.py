
import os

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"

def clear():
    if os.environ.get("TERM") and os.environ.get("TERM") != "dumb":
        os.system("clear")

def banner(version):
    print(CYAN + BOLD + r"""
 ____   _    _ _____ ____      _    _   _  _   _ _____ _____ ____  
|  _ \ / \  | | ____/ ___|    / \  | \ | || | | | ____| ____|  _ \ 
| |_) / _ \ | |  _|| |  _    / _ \ |  \| || |_| |  _| |  _| | |_) |
|  _ < ___ \| | |__| |_| |  / ___ \| |\  ||  _  | |___| |___|  _ <
|_| \_\_/  \_\_|_____\____| /_/   \_\_| \_|_| |_|_____|_____|_| \_\
""" + RESET)
    print(f"{BOLD}RAJA AI VIDEO ENHANCER{RESET}  {DIM}v{version} | Termux Edition{RESET}")
    print("-" * 62)

def status(label, ok, detail=""):
    color = GREEN if ok else YELLOW
    mark = "PASS" if ok else "CHECK"
    print(f"{color}[{mark}]{RESET} {label}" + (f" — {detail}" if detail else ""))

def menu():
    print("\n[1] Enhance one video (FFmpeg)")
    print("[2] Batch enhance a folder")
    print("[3] System / AI engine diagnostics")
    print("[4] View latest processing report")
    print("[5] Open project output folder")
    print("[0] Exit")
    return input("\nSelect: ").strip()
