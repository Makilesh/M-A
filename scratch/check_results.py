import json

with open("tests/e2e_validation_results.json", "r", encoding="utf-8") as f:
    res = json.load(f)

print(f"Total entries: {len(res)}")
for r in res:
    status = r.get("status")
    ans = r.get("answer", "")
    error = r.get("error", "")
    recall = r.get("recall_score", 0.0)
    cite = r.get("citation_match", False)
    
    if status == "passed":
        print(f"{r['id']}: PASSED | Recall: {recall*100:.1f}% | Citations: {cite} | Answer: {ans[:70].strip()}...")
    else:
        print(f"{r['id']}: FAILED ({status}) | Error: {error[:100]}...")
