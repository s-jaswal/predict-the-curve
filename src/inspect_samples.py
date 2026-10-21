import json
import os
from collections import Counter

from src.config import DATA_DIR

path = os.path.join(DATA_DIR, "samples.jsonl")
rows = [json.loads(line) for line in open(path, encoding="utf-8")]
n = len(rows)
print("run:", DATA_DIR)
print("records:", n)
print("stop reasons:", dict(Counter(r["stop_reason"] for r in rows)))
print("empty answers:", sum(1 for r in rows if not r["raw"].strip()))
print("block types:", dict(Counter(tuple(r["block_types"]) for r in rows)))
print("avg input tokens:", sum(r["input_tokens"] for r in rows) / n)
print("avg output tokens:", sum(r["output_tokens"] for r in rows) / n)
print("max output tokens:", max(r["output_tokens"] for r in rows))