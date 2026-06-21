import json
from pathlib import Path

log_path = Path(r"C:\Users\makil\.gemini\antigravity\brain\1b98f207-bb7d-499f-8f0f-cdc74424a847\.system_generated\tasks\task-1717.log")

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        if "quality_assessor" in line.lower() and "complete" in line.lower():
            print(line.strip())
        elif "structured agent call successful" in line.lower() and "gemini-3.1-flash-lite" in line.lower():
            print(line.strip())
