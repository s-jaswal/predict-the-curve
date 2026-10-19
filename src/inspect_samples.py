import json
from collections import Counter

rows = [json.loads(line) for line in open("data/samples.jsonl", encoding="utf-8")]
n = len(rows)
print("records:", n)
print("unique (problem, sample) pairs:",
      len({(r["problem_id"], r["sample_idx"]) for r in rows}))
print("stop reasons:", dict(Counter(r["stop_reason"] for r in rows)))
print("empty answers:", sum(1 for r in rows if not r["raw"].strip()))

with_tokens = [r for r in rows if "output_tokens" in r]
print("records with token info:", len(with_tokens), "of", n)

if with_tokens:
    m = len(with_tokens)
    print("avg input tokens:", sum(r["input_tokens"] for r in with_tokens) / m)
    print("avg output tokens:", sum(r["output_tokens"] for r in with_tokens) / m)
    print("max output tokens:", max(r["output_tokens"] for r in with_tokens))
    print()
    print("block types per problem (newer records only):")
    by_problem = {}
    for r in with_tokens:
        by_problem.setdefault(r["problem_id"], []).append(tuple(r["block_types"]))
    for pid, bt in sorted(by_problem.items()):
        print(" ", pid, dict(Counter(bt)))

print()
print("--- one sample answer ---")
print(rows[0]["raw"][:600])