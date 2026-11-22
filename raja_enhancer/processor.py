
import subprocess
from pathlib import Path
from .media import probe_video
from .logger import get_logger

log = get_logger()

def build_ffmpeg_command(source, destination, config, mode="balanced"):
    # Keep source dimensions unless larger than configured maximum; never upscale
    # and describe this conventional filter honestly (not AI super-resolution).
    scale = (
        f"scale=w='min({int(config['max_width'])},iw)':"
        f"h='min({int(config['max_height'])},ih)':"
        "force_original_aspect_ratio=decrease:force_divisible_by=2:flags=lanczos"
    )
    if mode == "light":
        vf = f"eq=contrast=1.03:saturation=1.04,{scale}"
    elif mode == "detail":
        vf = f"hqdn3d=1.2:1.2:4:4,unsharp=5:5:0.55:3:3:0.0,{scale}"
    else:
        vf = f"hqdn3d=1.5:1.5:6:6,unsharp=5:5:0.40:3:3:0.0,eq=contrast=1.02:saturation=1.03,{scale}"
    return [
        "ffmpeg", "-hide_banner", "-y" if config.get("overwrite") else "-n",
        "-i", str(source), "-vf", vf,
        "-c:v", config["video_codec"], "-preset", "veryfast",
        "-crf", str(int(config["crf"])),
        "-c:a", config["audio_codec"], "-b:a", config["audio_bitrate"],
        "-map_metadata", "0", "-movflags", "+faststart", str(destination)
    ]

def enhance_video(source, destination, config, mode="balanced"):
    source = Path(source)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    probe_video(source)
    command = build_ffmpeg_command(source, destination, config, mode)
    log.info("START | input=%s | output=%s | mode=%s", source, destination, mode)
    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode != 0:
        message = (completed.stderr or "FFmpeg failed")[-3000:]
        log.error("FAIL | input=%s | error=%s", source, message)
        raise RuntimeError(message)
    if not destination.exists() or destination.stat().st_size == 0:
        raise RuntimeError("FFmpeg returned success but output file is missing or empty")
    log.info("PASS | input=%s | output=%s | bytes=%s", source, destination, destination.stat().st_size)
    return {"input": str(source), "output": str(destination),
            "input_bytes": source.stat().st_size,
            "output_bytes": destination.stat().st_size,
            "mode": mode, "status": "PASS"}
