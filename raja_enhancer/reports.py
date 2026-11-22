
import json
from datetime import datetime
from .config import REPORT_DIR, ensure_directories

def write_report(results, started_at, finished_at):
    ensure_directories()
    passed = sum(1 for item in results if item.get("status") == "PASS")
    failed = len(results) - passed
    report = {
        "application": "RAJA AI VIDEO ENHANCER",
        "created_at": datetime.now().astimezone().isoformat(),
        "started_at": started_at,
        "finished_at": finished_at,
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "results": results
    }
    path = REPORT_DIR / f"report_{datetime.now():%Y%m%d_%H%M%S}.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return path

def latest_report():
    ensure_directories()
    reports = sorted(REPORT_DIR.glob("report_*.json"))
    if not reports:
        return None, None
    path = reports[-1]
    return path, json.loads(path.read_text(encoding="utf-8"))
