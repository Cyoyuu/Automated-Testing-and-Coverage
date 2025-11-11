import json
import os
import re

def extract_src(model, prompt, src="src", problem_set=[]):
    # Path to your JSONL file
    INPUT_FILE = f"example_results/{model}_results_{prompt}.jsonl"

    # Create the src folder if not exists
    os.makedirs(f"{model}_{prompt}_{src}", exist_ok=True)

    def sanitize_filename(name: str) -> str:
        """Ensure safe filenames (e.g., no slashes)."""
        return re.sub(r'[^a-zA-Z0-9_]', '_', name)

    # Read JSONL file line by line
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            item = json.loads(line)
            completion = item["completion"].strip()

            # Extract function name (assumes starts with "def func_name(")
            match = re.match(r"def\s+(\w+)\s*\(", completion)
            if not match:
                print(f"⚠️ Skipping invalid completion: {completion[:50]}...")
                continue
            func_name = match.group(1)
            filename = sanitize_filename(func_name)
            if problem_set and filename not in problem_set: continue

            # Write to src/filename.py
            output_path = os.path.join(f"{model}_{prompt}_{src}", f"{filename}.py")
            with open(output_path, "w", encoding="utf-8") as out:
                out.write(completion + "\n")

            print(f"✅ Wrote {output_path}")
    output_path = os.path.join(f"{model}_{prompt}_{src}", f"__init__.py")
    with open(output_path, "w", encoding="utf-8") as out:
        out.write("")

    print("\nAll src files created successfully.")

def extract_tests():

    # Path to your JSONL file
    INPUT_FILE = "humaneval_subset.jsonl"

    # Create output folder for tests
    os.makedirs("tests", exist_ok=True)

    # Read JSONL file line by line
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)

            entry = item["entry_point"]
            test_code = item["test"]

            # Build the Exercise 2–style pytest-compatible test file
            test_file_content = f"""import pytest
    from src.{entry} import {entry}

    {test_code}

    def test_all():
        check({entry})
    """

            # Write clean, runnable .py file (no escaped quotes or \n)
            test_path = os.path.join("tests", f"test_{entry}.py")
            with open(test_path, "w", encoding="utf-8") as out:
                out.write(test_file_content)

            print(f"✅ Wrote {test_path}")

    print("\nAll test files created successfully.")
