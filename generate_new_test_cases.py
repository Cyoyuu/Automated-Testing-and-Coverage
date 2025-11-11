import os
import sys
import argparse
import re
import dashscope
from dashscope import Generation

# Configure API key
dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")
if not dashscope.api_key:
    raise EnvironmentError("Please set DASHSCOPE_API_KEY environment variable.")

def extract_function_description(test_file_path: str) -> str:
    """Extract the function name and craft a description."""
    with open(test_file_path, 'r') as f:
        content = f.read()
    # Extract imported function name
    import_match = re.search(r'from\s+[\w\.]+\s+import\s+(\w+)', content)
    if not import_match:
        raise ValueError("Could not find imported function in test file.")
    func_name = import_match.group(1)
    return func_name

def read_existing_ret_statements(test_file_path: str) -> tuple:
    """Read existing ret+= lines and tot count."""
    with open(test_file_path, 'r') as f:
        content = f.read()

    # Extract function name
    func_name = extract_function_description(test_file_path)

    # Find the check function body
    check_match = re.search(r'def check\(candidate\):\s*\n(.*?)(?:\n\w|\Z)', content, re.DOTALL)
    if not check_match:
        raise ValueError("Could not find 'def check(candidate):' block.")

    check_body = check_match.group(1)
    lines = check_body.splitlines()

    # Extract existing ret+= lines and current tot
    ret_lines = []
    tot_count = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('ret+='):
            ret_lines.append(stripped)
        elif 'tot+=' in stripped:
            # Extract number after tot+=
            num_match = re.search(r'tot\+=\s*(\d+)', stripped)
            if num_match:
                tot_count += int(num_match.group(1))

    return func_name, ret_lines, tot_count

def generate_prompt(func_name: str, existing_ret_count: int) -> str:
    descriptions = {
        "rounded_avg": '''
def rounded_avg(n, m):
    """
    Given two integers n and m (n <= m), compute the average of all integers from n to m inclusive,
    round it to the nearest integer, and return its binary representation as a string prefixed with '0b'.
    If n > m, return -1.
    """
''',
        "move_one_ball": '''
def move_one_ball(arr):
    """
    We have an array 'arr' of N integers arr[1], arr[2], ..., arr[N].The    numbers in the array will be randomly ordered. Your task is to determine if    it is possible to get an array sorted in non-decreasing order by performing     the following operation on the given array:        You are allowed to perform right shift operation any number of times.        One right shift operation means shifting all elements of the array by one    position in the right direction. The last element of the array will be moved to    the starting position in the array i.e. 0th index.     If it is possible to obtain the sorted array by performing the above operation    then return True else return False.    If the given array is empty then return True.    Note: The given list is guaranteed to have unique elements.    For Example:        move_one_ball([3, 4, 5, 1, 2])==>True    Explanation: By performin 2 right shift operations, non-decreasing order can                 be achieved for the given array.    move_one_ball([3, 5, 4, 1, 2])==>False    Explanation:It is not possible to get non-decreasing order for the given                array by performing any number of right shift operations. 
    """
'''
    }

    desc = descriptions.get(func_name, f"Function {func_name} (no description available).")

    prompt = f"""You are an expert Python engineer generating unit tests in a specific format.

{desc}

Current tests use a 'check' function with 'ret+=' and 'tot+=' (NO 'assert').

Your task: Generate **additional test cases** as 'ret+=' lines that improve **branch and condition coverage**.
Focus on edge cases like:
- Boundary values (min/max inputs)
- Error conditions (e.g., n > m for rounded_avg)
- Empty or extreme ranges
- Rounding behavior (midpoints, even/odd averages)

Rules:
- Output ONLY the new 'ret+=' lines, one per line.
- Do NOT include 'tot+=' or function definitions.
- Do NOT use 'assert'.
- Each line must be of the form: ret+=candidate(...) == ...
- Use correct expected outputs.

Example for rounded_avg:
ret+=candidate(1, 1) == "0b1"
ret+=candidate(5, 3) == -1
"""
    return prompt

def call_qwen(prompt: str, model="qwen-max") -> str:
    response = Generation.call(
        model=model,
        prompt=prompt,
        temperature=0.2,
        max_tokens=500,
        result_format="text"
    )
    if response.status_code != 200:
        raise RuntimeError(f"Qwen error: {response}")
    text = response.output.text.strip()
    # Remove markdown if present
    if text.startswith("```"):
        text = re.split(r"```(?:python)?", text, 1)[-1]
        text = text.split("```")[0].strip()
    return text

def write_new_test_file(
    original_path: str,
    output_path: str,
    new_ret_lines: list,
    original_ret_lines: list,
    original_tot: int
):
    with open(original_path, 'r') as f:
        original_content = f.read()

    # Determine function name
    func_name = extract_function_description(original_path)

    # Combine all ret lines
    all_ret_lines = original_ret_lines + new_ret_lines
    new_tot = original_tot + len(new_ret_lines)

    # Rebuild check function
    check_code = "def check(candidate):\n"
    check_code += "    ret, tot=0, 0\n\n"
    check_code += "    # Check some simple cases\n"
    for line in all_ret_lines:
        check_code += f"    {line}\n"
    check_code += f"    tot+={new_tot}\n"
    check_code += "    return ret/tot\n"

    # Rebuild full file
    import_line_match = re.search(r'(import pytest\s*\nfrom\s+[\w\.]+\s+import\s+\w+)', original_content)
    if not import_line_match:
        raise ValueError("Could not find import header.")

    header = import_line_match.group(1)
    new_content = f"{header}\n\n{check_code}\n\ndef test_all():\n    return check({func_name})\n"

    with open(output_path, 'w') as f:
        f.write(new_content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', required=True, help='Directory containing original test files')
    parser.add_argument('--output_dir', required=True, help='Directory to save augmented test files')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    for filename in os.listdir(args.input_dir):
        if not filename.startswith("test_") or not filename.endswith(".py"):
            continue
        if filename not in ['test_rounded_avg.py']: continue
        print(filename)

        input_path = os.path.join(args.input_dir, filename)
        output_path = os.path.join(args.output_dir, filename)

        try:
            print(f"Processing: {filename}")
            func_name, existing_ret, tot = read_existing_ret_statements(input_path)
            prompt = generate_prompt(func_name, tot)
            print("Prompting Qwen...")
            new_lines_text = call_qwen(prompt)
            # Parse new ret+= lines
            new_ret_lines = []
            for line in new_lines_text.splitlines():
                line = line.strip()
                if line.startswith("ret+="):
                    # Validate syntax roughly
                    if "candidate(" in line and ("==" in line or "!=" in line):
                        new_ret_lines.append(line)
            print(f"Generated {len(new_ret_lines)} new test lines.")

            write_new_test_file(input_path, output_path, new_ret_lines, existing_ret, tot)
            print(f"Saved augmented test to: {output_path}\n")

        except Exception as e:
            print(f"❌ Failed on {filename}: {e}")

if __name__ == "__main__":
    main()