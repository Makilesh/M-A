import json

with open("tests/e2e_validation_results.json", "r", encoding="utf-8") as f:
    res = json.load(f)

fin_03 = next(r for r in res if r["id"] == "fin_03")
print("AGENT TRACE FOR fin_03:")
print(json.dumps(fin_03.get("agent_trace"), indent=2))
