from human_eval.data import read_problems

problems = read_problems()
print(len(problems))  # should show 164

k = 10  # number of tasks you want
subset = list(problems.items())[100:110]
print(subset)

import json

with open("humaneval_subset_tmp.jsonl", "w") as f:
    for task in subset:
        task[1].pop('entry_point')
        # task[1].pop('test')
        task[1].pop('canonical_solution')
        f.write(json.dumps(task[1]) + "\n")
