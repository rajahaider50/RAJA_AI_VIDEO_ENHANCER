
from pathlib import Path
import json

APP_NAME = "RAJA AI VIDEO ENHANCER"
APP_VERSION = "1.0.0"
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = DATA_DIR / "logs"
REPORT_DIR = DATA_DIR / "reports"
OUTPUT_DIR = BASE_DIR / "output"
CONFIG_FILE = DATA_DIR / "config.json"
SUPPORTED_EXTENSIONS = {".mp4", ".mkv", ".mov", ".webm", ".avi", ".m4v"}

DEFAULT_CONFIG = {
    "output_dir": str(OUTPUT_DIR),
    "preset": "balanced",
    "crf": 19,
    "video_codec": "libx264",
    "audio_codec": "aac",
    "audio_bitrate": "192k",
    "max_width": 1920,
    "max_height": 1080,
    "overwrite": False
}

def ensure_directories():
    for path in (DATA_DIR, LOG_DIR, REPORT_DIR, OUTPUT_DIR):
        path.mkdir(parents=True, exist_ok=True)

def load_config():
    ensure_directories()
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        merged = DEFAULT_CONFIG.copy()
        merged.update(data)
        return merged
    except (OSError, json.JSONDecodeError):
        return DEFAULT_CONFIG.copy()

def save_config(data):
    ensure_directories()
    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
