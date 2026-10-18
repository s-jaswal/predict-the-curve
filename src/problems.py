
import random
from datasets import load_dataset


def load_problems(n=50, seed=42):
    ds = load_dataset("openai/openai_humaneval", split="test")
    problems = [
        {
            "id": row["task_id"],
            "prompt": row["prompt"],
            "test": row["test"],
            "entry_point": row["entry_point"],
            "canonical_solution": row["canonical_solution"],
        }
        for row in ds
    ]
    random.Random(seed).shuffle(problems)
    return problems[:n]


def build_prompt(problem):
    return (
        "Complete the following Python function. "
        "Return the full function in a single ```python code block, "
        "with no explanation.\n\n" + problem["prompt"]
    )


def build_test_program(problem, code):
    # The original prompt goes first so imports and helper functions
    # exist, then the model's full definition overrides the stub.
    return (
        problem["prompt"] + "\n    pass\n\n"
        + code + "\n\n"
        + problem["test"] + "\n\n"
        + f"check({problem['entry_point']})\n"
    )


if __name__ == "__main__":
    probs = load_problems(n=3)
    for p in probs:
        print(p["id"], p["entry_point"])
    print(build_prompt(probs[0]))