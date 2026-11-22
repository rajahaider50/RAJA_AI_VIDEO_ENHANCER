
import shutil
import subprocess
import platform
from .ui import status

def _version(command):
    try:
        p = subprocess.run([command, "-version"], capture_output=True, text=True, timeout=10)
        first = (p.stdout or p.stderr).splitlines()
        return first[0] if first else "available"
    except Exception as exc:
        return str(exc)

def run_diagnostics():
    print("\n--- Environment diagnostics ---")
    for cmd in ("python", "ffmpeg", "ffprobe"):
        path = shutil.which(cmd)
        status(cmd, bool(path), path or "not found")
        if path and cmd in ("ffmpeg", "ffprobe"):
            print("   " + _version(cmd))
    print(f"Platform: {platform.platform()}")
    print("\n--- Optional AI engines ---")
    for cmd in ("realesrgan-ncnn-vulkan", "rife-ncnn-vulkan"):
        path = shutil.which(cmd)
        status(cmd, bool(path), path or "not installed")
    print("\nImportant: detecting an AI executable does not prove GPU compatibility.")
    print("This release does not claim AI enhancement unless an AI pipeline is installed.")
