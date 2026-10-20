import json
import os
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from src.config import DATA_DIR
from src.problems import load_problems, build_test_program
from src.executor import extract_code, run_program

SAMPLES = os.path.join(DATA_DIR, "samples.jsonl")
GRADES = os.path.join(DATA_DIR, "grades.jsonl")
RESULTS = os.path.join(DATA_DIR, "results.json")


def grade_record(rec, problem):
    code = extract_code(rec["raw"])
    ok = run_program(build_test_program(problem, code))
    return {"problem_id": rec["problem_id"],
            "sample_idx": rec["sample_idx"], "passed": ok}


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

    with ThreadPoolExecutor(8) as pool, \
            open(GRADES, "a", encoding="utf-8") as out:
        futures = [pool.submit(grade_record, r, problems[r["problem_id"]])
                   for r in todo]
        for fut in futures:
            out.write(json.dumps(fut.result()) + "\n")
            out.flush()

    counts = defaultdict(lambda: {"n": 0, "c": 0})
    with open(GRADES, encoding="utf-8") as f:
        for r in map(json.loads, f):
            if r["problem_id"] in problems:
                counts[r["problem_id"]]["n"] += 1
                counts[r["problem_id"]]["c"] += int(r["passed"])

    with open(RESULTS, "w", encoding="utf-8") as f:
        json.dump(counts, f, indent=2)
    for pid, v in sorted(counts.items()):
        print(pid, f'{v["c"]}/{v["n"]}')


if __name__ == "__main__":
    main(int(sys.argv[1]))