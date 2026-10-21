import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import anthropic

from src.config import MODEL, DATA_DIR
from src.math_problems import load_problems, build_prompt

CACHE = os.path.join(DATA_DIR, "samples.jsonl")
SAMPLING_KWARGS = {"extra_body": {"temperature": 1.0}}

client = anthropic.Anthropic(max_retries=5)


def load_done():
    if not os.path.exists(CACHE):
        return set()
    with open(CACHE, encoding="utf-8") as f:
        return {(r["problem_id"], r["sample_idx"]) for r in map(json.loads, f)}


def sample_one(problem, idx):
    resp = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        messages=[{"role": "user", "content": build_prompt(problem)}],
        **SAMPLING_KWARGS,
    )
    text = "".join(b.text for b in resp.content if b.type == "text")
    return {
        "problem_id": problem["id"],
        "sample_idx": idx,
        "model": MODEL,
        "raw": text,
        "stop_reason": resp.stop_reason,
        "input_tokens": resp.usage.input_tokens,
        "output_tokens": resp.usage.output_tokens,
        "block_types": [b.type for b in resp.content],
    }


def main(n_problems, n_samples, workers=8):
    problems = load_problems(n=n_problems)
    done = load_done()
    jobs = [(p, i) for p in problems for i in range(n_samples)
            if (p["id"], i) not in done]
    print(f"run={DATA_DIR} model={MODEL}")
    print(f"{len(jobs)} calls to make ({len(done)} already cached)")

    os.makedirs(DATA_DIR, exist_ok=True)
    with ThreadPoolExecutor(workers) as pool, \
            open(CACHE, "a", encoding="utf-8") as out:
        futures = {pool.submit(sample_one, p, i): (p["id"], i)
                   for p, i in jobs}
        for n, fut in enumerate(as_completed(futures), 1):
            try:
                rec = fut.result()
            except Exception as e:
                print("FAILED", futures[fut], e)
                continue
            out.write(json.dumps(rec) + "\n")
            out.flush()
            if n % 25 == 0:
                print(f"{n}/{len(jobs)}")


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))