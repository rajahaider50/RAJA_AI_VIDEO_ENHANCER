
from datetime import datetime
from pathlib import Path
import os
import subprocess
import sys

from . import __version__
from .config import APP_NAME, OUTPUT_DIR, load_config
from .diagnostics import run_diagnostics
from .logger import get_logger
from .media import validate_video, find_videos
from .processor import enhance_video
from .reports import write_report, latest_report
from .ui import banner, menu, status

log = get_logger()

def choose_mode():
    print("\nProcessing profile:")
    print("[1] Light — mild color/contrast")
    print("[2] Balanced — denoise + mild sharpen")
    print("[3] Detail — stronger denoise + sharpen")
    choice = input("Choose [2]: ").strip() or "2"
    return {"1": "light", "2": "balanced", "3": "detail"}.get(choice, "balanced")

def process_one(config):
    raw = input("\nVideo path (you can paste full path): ").strip().strip('"').strip("'")
    if not raw:
        return
    try:
        source = validate_video(raw)
        mode = choose_mode()
        destination = Path(config["output_dir"]) / f"{source.stem}_raja_enhanced.mp4"
        if destination.exists() and not config.get("overwrite"):
            destination = destination.with_name(f"{source.stem}_raja_enhanced_{datetime.now():%H%M%S}.mp4")
        result = enhance_video(source, destination, config, mode)
        report = write_report([result], datetime.now().astimezone().isoformat(),
                              datetime.now().astimezone().isoformat())
        status("Video processed", True, str(destination))
        print(f"Report: {report}")
    except Exception as exc:
        log.exception("Single-video processing failed")
        print(f"\n[ERROR] {exc}")
        report = write_report([{"input": raw, "status": "FAIL", "error": str(exc)}],
                              datetime.now().astimezone().isoformat(),
                              datetime.now().astimezone().isoformat())
        print(f"Failure recorded: {report}")

def process_batch(config):
    raw = input("\nFolder containing videos: ").strip().strip('"').strip("'")
    if not raw:
        return
    started = datetime.now().astimezone().isoformat()
    results = []
    try:
        videos = find_videos(raw)
        if not videos:
            print("No supported videos found.")
            return
        mode = choose_mode()
        print(f"\nFound {len(videos)} video(s). Processing sequentially...")
        for index, source in enumerate(videos, 1):
            destination = Path(config["output_dir"]) / f"{source.stem}_raja_enhanced.mp4"
            if destination.exists() and not config.get("overwrite"):
                destination = destination.with_name(f"{source.stem}_raja_enhanced_{datetime.now():%H%M%S}.mp4")
            print(f"\n[{index}/{len(videos)}] {source.name}")
            try:
                result = enhance_video(source, destination, config, mode)
                results.append(result)
                status(source.name, True, destination.name)
            except Exception as exc:
                log.exception("Batch item failed: %s", source)
                results.append({"input": str(source), "status": "FAIL", "error": str(exc)})
                status(source.name, False, str(exc)[:160])
        report = write_report(results, started, datetime.now().astimezone().isoformat())
        passed = sum(x["status"] == "PASS" for x in results)
        failed = len(results) - passed
        print(f"\nBatch complete: {passed} passed, {failed} failed.")
        print(f"Report saved: {report}")
    except Exception as exc:
        print(f"[ERROR] {exc}")

def show_latest_report():
    path, data = latest_report()
    if not path:
        print("No reports yet.")
        return
    print(f"\nLatest report: {path}")
    print(f"Total: {data['total']} | Passed: {data['passed']} | Failed: {data['failed']}")
    for item in data["results"]:
        print(f"- {item.get('status')} | {Path(item.get('input', '?')).name}")
        if item.get("error"):
            print(f"  Error: {item['error']}")

def open_output():
    folder = Path(load_config()["output_dir"]).expanduser()
    folder.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(["termux-open", str(folder)], check=False)
    except FileNotFoundError:
        print(f"Output folder: {folder}")

def main():
    config = load_config()
    while True:
        banner(__version__)
        choice = menu()
        if choice == "1":
            process_one(config)
        elif choice == "2":
            process_batch(config)
        elif choice == "3":
            run_diagnostics()
        elif choice == "4":
            show_latest_report()
        elif choice == "5":
            open_output()
        elif choice == "0":
            print("Thank you for using " + APP_NAME)
            return 0
        else:
            print("Invalid option.")
        input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    raise SystemExit(main())
