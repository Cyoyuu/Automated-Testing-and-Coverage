# Code-Generation-with-LLMs (Exercise 1 Part)

CS 520 Project

# How to run

First export your api key to the env and then run `generate_result.sh ${MODEL} ${METHOD}`.

Second, run `evaluate.py` and change the `sample_file` path to your wanted one.

# Where is the example results

Example results are in the `example_results` folder.

# Automated-Testing-and-Coverage (Exercise 2 Part)

# How to run

run `text.py`.

If you want results in the report:

run `python test.py -m qwen -p self_planning -v ...`

select `-v` from nothing for original coverage, `_up1` for improvement iteration 1, `_up2` for improvement iteration 2.

# generating test cases

run `generate_new_test_cases.py`, specifying the input dir like `tests` and the output dir like `tests_up1`.