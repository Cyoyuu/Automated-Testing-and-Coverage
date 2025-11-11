import os
import sys
import argparse
import subprocess
import xml.etree.ElementTree as ET
import re
import csv
from extract_src import *

# ---------------------------
# Helper: parse coverage.xml
# ---------------------------
def parse_coverage_xml(xml_path): 
    """Parse coverage.xml and summarize line & branch coverage per file.""" 
    if not os.path.exists(xml_path): 
        print("⚠️ coverage.xml not found, skipping summary table.") 
        return [] 
    tree = ET.parse(xml_path) 
    root = tree.getroot() 
    summary = [] 
    for cls in root.findall(".//class"): 
        filename = cls.get("filename", "unknown") 
        line_rate = float(cls.attrib.get("line-rate", "0")) * 100 
        branch_rate = float(cls.attrib.get("branch-rate", "0")) * 100 
        summary.append({ "file": filename, "line_coverage": line_rate, "branch_coverage": branch_rate, }) 
    return summary


# ---------------------------
# Helper: extract pass rate (ret/tot) from test
# ---------------------------
def extract_pass_rate(test_file, model, prompt):
    """
    Run the test file directly and capture the return value of check()
    e.g., ret/tot ratio
    """
    try:
        with open(test_file, "r") as f:
            code = f.read()
        # find function name under "from src.xxx import yyy"
        match = re.search(rf"from {model}_{prompt}_src\.(\w+) import (\w+)", code)
        if not match:
            return 0.0
        src_module, func_name = match.groups()

        # dynamically run code and get result of check()
        globals_dict = {}
        locals_dict = {}
        exec(code, globals_dict, locals_dict)
        if "check" in locals_dict:
            # dummy import for source
            sys.path.insert(0, os.path.abspath(f"{model}_{prompt}_src"))
            src_mod = __import__(src_module)
            candidate = getattr(src_mod, func_name)
            val = locals_dict["check"](candidate)
            if isinstance(val, (int, float)):
                return round(float(val), 2)
    except Exception as e:
        print(f"⚠️ Error running {test_file}: {e}")
    return 0.0

import shutil
import re

def copy_and_rewrite_tests(src_folder, dest_folder, model, prompt, problem_set=[]):
    """
    Copy the test folder and rewrite all 'from src.xxx import yyy'
    to 'from {model}_{prompt}_src.xxx import yyy'
    """
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
    shutil.copytree(src_folder, dest_folder)

    pattern = re.compile(r"from\s+src(\.[\w_]+)\s+import\s+([\w_]+)")

    for root, _, files in os.walk(dest_folder):
        for fname in files:
            if not fname.endswith(".py"):
                continue
            if problem_set and fname not in problem_set: continue
            fpath = os.path.join(root, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                code = f.read()
            # Replace 'from src.xxx import yyy'
            new_code = re.sub(
                pattern,
                lambda m: f"from {model}_{prompt}_src{m.group(1)} import {m.group(2)}",
                code,
            )
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_code)

def write_summary(summary, output_dir):
    """Write coverage summary to Markdown and CSV."""
    if not summary:
        return

    md_path = os.path.join(output_dir, "coverage_summary.md")
    csv_path = os.path.join(output_dir, "coverage_summary.csv")

    with open(md_path, "w") as md:
        md.write("| File | Line Coverage (%) | Branch Coverage (%) |\n")
        md.write("|------|-------------------|--------------------|\n")
        for item in summary:
            md.write(f"| {item['file']} | {item['line_coverage']:.1f} | {item['branch_coverage']:.1f} |\n")

    with open(csv_path, "w", newline="") as csvf:
        writer = csv.DictWriter(csvf, fieldnames=["file", "line_coverage", "branch_coverage"])
        writer.writeheader()
        writer.writerows(summary)

    print(f"📊 Coverage summary saved to:\n  - {md_path}\n  - {csv_path}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", type=str, choices=['gpt', 'qwen'])
    parser.add_argument("--prompt", "-p", type=str, choices=['self_planning', 'self_debugging'])
    parser.add_argument("--version", "-v", type=str, default='', choices=['', '_up1', '_up2'])
    args = parser.parse_args()
    if args.version=='_up2':
        problem_set = ['rounded_avg']
    elif args.version=='_up1':
        problem_set = ['rounded_avg', 'move_one_ball']
    else:
        problem_set = []
    # extract_src(args.model, args.prompt, src="src_up2", problem_set=problem_set)
    # copy_and_rewrite_tests('tests_up2', f"{args.model}_{args.prompt}_tests_up2", args.model, args.prompt, problem_set=problem_set)
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(project_root, f"{args.model}_{args.prompt}_src{args.version}")
    tests_path = os.path.join(project_root, f"{args.model}_{args.prompt}_tests{args.version}")

    sys.path.insert(0, src_path)
    os.environ["PYTHONPATH"] = project_root

    htmlcov_dir = os.path.join(project_root, "htmlcov")
    os.makedirs(htmlcov_dir, exist_ok=True)

    if not os.path.exists(src_path):
        print(f"❌ Error: '{args.model}_{args.prompt}_src/' folder not found.")
        sys.exit(1)
    if not os.path.exists(tests_path):
        print("❌ Error: 'tests/' folder not found.")
        sys.exit(1)

    results = []

    # Step 1. Run pytest with coverage for the specific test
    xml_path = os.path.join(project_root, "coverage.xml")
    if os.path.exists(xml_path):
        os.remove(xml_path)

    cmd = [
        sys.executable,
        "-m", "pytest",
        "--maxfail=1",
        "--disable-warnings",
        f"--cov={args.model}_{args.prompt}_src{args.version}",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-report=xml",
        "--cov-branch",
        tests_path
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    summary = parse_coverage_xml(xml_path=xml_path)
    print(f"summary: {summary}")

    idx=0
    for test_file in sorted(os.listdir(tests_path)):
        if not test_file.endswith(".py"):
            continue

        test_name = test_file.replace(".py", "")
        test_path = os.path.join(tests_path, test_file)

        print(f"🧪 Running {test_name} ...")
        if os.path.exists(".coverage"):
                os.remove(".coverage")

        # Step 2. Parse coverage
        print(summary[idx]['file'])
        line_cov, branch_cov = summary[idx]['line_coverage'], summary[idx]['branch_coverage']

        # Step 3. Compute pass rate via ret/tot
        pass_rate = extract_pass_rate(test_path, args.model, args.prompt)

        # Step 4. Create one-line summary
        if branch_cov < 50:
            interpretation = "Low branch coverage, likely missing conditional paths"
        elif line_cov < 80:
            interpretation = "Moderate coverage, could improve with more tests"
        else:
            interpretation = "Good overall coverage"

        results.append({
            "test_name": test_name,
            "pass_rate": pass_rate,
            "line_cov": round(line_cov, 2),
            "branch_cov": round(branch_cov, 2),
            "interpretation": interpretation
        })
        idx+=1

    # Step 5. Output summary table
    print("\n=== 📊 Summary ===")
    for r in results:
        print(f"{r['test_name']}: passed={r['pass_rate']*100:.0f}%, "
              f"line_cov={r['line_cov']}%, branch_cov={r['branch_cov']}% — {r['interpretation']}")

    # Step 6. Save results to CSV and Markdown
    csv_path = os.path.join(project_root, f"results_{args.model}_{args.prompt}.csv")
    md_path = os.path.join(project_root, f"results_{args.model}_{args.prompt}.md")

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["test_name", "pass_rate", "line_cov", "branch_cov", "interpretation"])
        writer.writeheader()
        writer.writerows(results)

    if os.path.exists("coverage.json"):
        with open("coverage.json", "r") as f:
            data = json.load(f)
    else:
        data = {}

    with open("coverage.json", "w") as f:
        for key in results:
            if key['test_name'] not in data: data[key['test_name']]={}
            data[key['test_name']][f"{args.model}_{args.prompt}"]=key
        json.dump(data, f, indent=2)

    with open(md_path, "w") as f:
        f.write("| Test | Pass Rate | Line Coverage | Branch Coverage | Interpretation |\n")
        f.write("|------|------------|----------------|-----------------|----------------|\n")
        for r in results:
            f.write(f"| {r['test_name']} | {r['pass_rate']*100:.0f}% | "
                    f"{r['line_cov']}% | {r['branch_cov']}% | {r['interpretation']} |\n")

    print(f"\n✅ Results saved to:\n  - {csv_path}\n  - {md_path}\n")


if __name__ == "__main__":
    main()
