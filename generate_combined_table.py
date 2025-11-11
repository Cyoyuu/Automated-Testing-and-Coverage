import json

def generate_combined_table(json_path, output_path="combined_coverage_table.tex"):
    with open(json_path, "r") as f:
        data = json.load(f)

    with open(output_path, "w") as tex:
        tex.write("\\documentclass{article}\n")
        tex.write("\\usepackage{booktabs}\n")
        tex.write("\\usepackage{tabularx}\n")
        tex.write("\\usepackage[a4paper,margin=1in]{geometry}\n\n")
        tex.write("\\begin{document}\n\n")
        tex.write("\\section*{Overall Coverage and Test Summary}\n\n")
        tex.write("\\begin{table}[h!]\n")
        tex.write("\\centering\n")
        tex.write("\\renewcommand{\\arraystretch}{1.3}\n")
        tex.write("\\begin{tabularx}{\\textwidth}{llccccX}\n")
        tex.write("\\toprule\n")
        tex.write("\\textbf{Test Name} & \\textbf{Model–Prompt} & "
                  "\\textbf{Pass Rate (\\%)} & \\textbf{Line Cov. (\\%)} & "
                  "\\textbf{Branch Cov. (\\%)} & \\textbf{Interpretation} \\\\\n")
        tex.write("\\midrule\n")

        order = ["gpt_self_planning", "gpt_self_debugging",
                 "qwen_self_planning", "qwen_self_debugging"]

        for test_name, models in data.items():
            for key in order:
                if key in models:
                    entry = models[key]
                    model_prompt = key.replace("_", " ").title()
                    tex.write(f"{test_name.replace('_', ' ')} & "
                              f"{model_prompt} & "
                              f"{entry['pass_rate']*100:.0f} & "
                              f"{entry['line_cov']:.2f} & "
                              f"{entry['branch_cov']:.2f} & "
                              f"{entry['interpretation']} \\\\\n")

        tex.write("\\bottomrule\n")
        tex.write("\\end{tabularx}\n")
        tex.write("\\caption{Combined coverage, pass rate, and interpretation summary "
                  "across all problems, models, and prompts.}\n")
        tex.write("\\end{table}\n\n")
        tex.write("\\end{document}\n")

    print(f"✅ Overleaf-ready LaTeX file generated: {output_path}")


# Example usage:
generate_combined_table("coverage.json")
