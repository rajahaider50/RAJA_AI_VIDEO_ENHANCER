
import json
import subprocess
from pathlib import Path
from .config import SUPPORTED_EXTENSIONS

def probe_video(path):
    command = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate",
        "-of", "json", str(path)
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe failed")
    return json.loads(result.stdout)

def validate_video(path):
    p = Path(path).expanduser()
    if not p.is_file():
        raise FileNotFoundError(f"Video not found: {p}")
    if p.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported extension: {p.suffix}")
    return p.resolve()

def find_videos(folder):
    p = Path(folder).expanduser()
    if not p.is_dir():
        raise NotADirectoryError(str(p))
    return sorted(x for x in p.iterdir() if x.is_file() and x.suffix.lower() in SUPPORTED_EXTENSIONS)
