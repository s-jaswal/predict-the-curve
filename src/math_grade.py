import json
import os
import sys
from collections import defaultdict

from src.config import DATA_DIR
from src.math_problems import load_problems, last_boxed, is_correct

SAMPLES = os.path.join(DATA_DIR, "samples.jsonl")
GRADES = os.path.join(DATA_DIR, "grades.jsonl")
RESULTS = os.path.join(DATA_DIR, "results.json")


def main(n_problems):
    problems = {p["id"]: p for p in load_problems(n=n_problems)}

    done = set()
    if os.path.exists(GRADES):
        with open(GRADES, encoding="utf-8") as f:
            done = {(r["problem_id"], r["sample_idx"])
                    for r in map(json.loads, f)}

    with open(SAMPLES, encoding="utf-8") as f:
        todo = [r for r in map(json.loads, f)
                if r["problem_id"] in problems
                and (r["problem_id"], r["sample_idx"]) not in done]
    print(f"run={DATA_DIR}")
    print(f"{len(todo)} samples to grade ({len(done)} already graded)")

    with open(GRADES, "a", encoding="utf-8") as out:
        for r in todo:
            gold = problems[r["problem_id"]]["answer"]
            rec = {
                "problem_id": r["problem_id"],
                "sample_idx": r["sample_idx"],
                "passed": is_correct(r["raw"], gold),
                "pred": last_boxed(r["raw"]),
                "gold": gold,
            }
            out.write(json.dumps(rec) + "\n")

    counts = defaultdict(lambda: {"n": 0, "c": 0})
    with open(GRADES, encoding="utf-8") as f:
        for r in map(json.loads, f):
            if r["problem_id"] in problems:
                counts[r["problem_id"]]["n"] += 1
                counts[r["problem_id"]]["c"] += int(r["passed"])

    with open(RESULTS, "w", encoding="utf-8") as f:
        json.dump(counts, f, indent=2)
    print("graded problems:", len(counts))


if __name__ == "__main__":
    main(int(sys.argv[1]))