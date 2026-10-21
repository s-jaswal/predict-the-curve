import json
import os
from collections import defaultdict

from src.config import DATA_DIR

path = os.path.join(DATA_DIR, "grades.jsonl")
rows = [json.loads(line) for line in open(path, encoding="utf-8")]
by_problem = defaultdict(list)
for r in rows:
    by_problem[r["problem_id"]].append(r)

for pid, rs in sorted(by_problem.items()):
    c = sum(r["passed"] for r in rs)
    if c < len(rs):
        print(pid, f"{c}/{len(rs)}", "| gold:", rs[0]["gold"])
        shown = 0
        for r in rs:
            if not r["passed"] and shown < 2:
                print("      model said:", r["pred"])
                shown += 1