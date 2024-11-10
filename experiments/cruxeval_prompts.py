# Reference: https://github.com/facebookresearch/cruxeval/blob/main/prompts.py

def make_cot_output_prompt(s):
    code, input = s
    return f"""You are given a Python function and an assertion containing an input to the function. Complete the assertion with a literal (no unsimplified expressions, no function calls) containing the output when executing the provided code on the given input, even if the function is incorrect or incomplete. Do NOT output any extra information. Execute the program step by step before arriving at an answer, and provide the full assertion with the correct output in [ANSWER] and [/ANSWER] tags, following the examples.

[PYTHON]
def f(s):
    s = s + s
    return "b" + s + "a"
assert f("hi") == ??
[/PYTHON]
[THOUGHT]
Let's execute the code step by step:

1. The function f is defined, which takes a single argument s.
2. The function is called with the argument "hi", so within the function, s is initially "hi".
3. Inside the function, s is concatenated with itself, so s becomes "hihi".
4. The function then returns a new string that starts with "b", followed by the value of s (which is now "hihi"), and ends with "a".
5. The return value of the function is therefore "bhihia".
[/THOUGHT]
[ANSWER]
assert f("hi") == "bhihia"
[/ANSWER]

[PYTHON]
{code}
assert f({input}) == ??
[/PYTHON]
[THOUGHT]
"""

def make_forward_monologue_output_prompt(s, prefix=False, version="v1.5"):
    special_token = "[SCRACHPAD]" if version == "v1" else "[MONOLOGUE]"
    code, input = s
    if not prefix:
        return f"""
[PYTHON]
{code}
assert f({input}) == ??
[/PYTHON]
{special_token}
"""
    else:
        return f"""Simulate the Execution: You are given a Python function and an assertion containing a function input. Complete the assertion containing the execution output corresponding to the given input in [ANSWER] and [/ANSWER] tags.
[PYTHON]
{code}
assert f({input}) == ??
[/PYTHON]
{special_token}
"""


def make_direct_output_prompt(s):
    code, input = s
    return f"""You are given a Python function and an assertion containing an input to the function. Complete the assertion with a literal (no unsimplified expressions, no function calls) containing the output when executing the provided code on the given input, even if the function is incorrect or incomplete. Do NOT output any extra information. Provide the full assertion with the correct output in [ANSWER] and [/ANSWER] tags, following the examples.

[PYTHON]
def f(n):
    return n
assert f(17) == ??
[/PYTHON]
[ANSWER]
assert f(17) == 17
[/ANSWER]

[PYTHON]
def f(s):
    return s + "a"
assert f("x9j") == ??
[/PYTHON]
[ANSWER]
assert f("x9j") == "x9ja"
[/ANSWER]

[PYTHON]
{code}
assert f({input}) == ??
[/PYTHON]
[ANSWER]
"""

def make_direct_input_prompt(s):
    code, output = s
    return f"""You will be given a function and an output in the form function(??) == output. Find any input such that executing function on the input leads to the given output. There may be multiple answers, but you should only output one. In [ANSWER] and [/ANSWER] tags, complete the assertion with one such input that will produce the output when executing the function.

[PYTHON]
def f(my_list):
    count = 0
    for i in my_list:
        if len(i) % 2 == 0:
            count += 1
    return count
assert f(??) == 3
[/PYTHON]
[ANSWER]
assert f(["mq", "px", "zy"]) == 3
[/ANSWER]

[PYTHON]
def f(s1, s2):
    return s1 + s2
assert f(??) == "banana"
[/PYTHON]
[ANSWER]
assert f("ba", "nana") == "banana"
[/ANSWER]

[PYTHON]
{code}
assert f(??) == {output}
[/PYTHON]
[ANSWER]
"""

def make_cot_input_prompt(s):
    code, output = s
    return f"""You will be given a function and an output in the form function(??) == output. Your task is to find any input such that executing function on the input leads to the given output. There may be multiple answers, but only output one. First, think step by step. You MUST surround the answer with [ANSWER] and [/ANSWER] tags. Express your answer as a passing assertion containing the input and the given output.

[PYTHON]
def f(x):
    return x + 1
assert f(??) == 17
[/PYTHON]
[THOUGHT]
To find an input such that executing f on the input leads to the given output, we can work backwards from the given assertion. We know that f(??) == 17. 

Since the function f(x) returns x + 1, for f(??) to be equal to 17, the value of ?? should be 16. 
[/THOUGHT]
[ANSWER]
assert f(16) == 17
[/ANSWER]

[PYTHON]
{code}
assert f(??) == {output}
[/PYTHON]
[THOUGHT]
"""


def make_backward_monologue_input_prompt(s, prefix=False, version="v1.5"):
    special_token = "[DEDUCTION]" if version == "v1" else "[MONOLOGUE]"
    code, output = s
    if not prefix:
        return f"""
[PYTHON]
{code}
assert f(??) == {output}
[/PYTHON]

{special_token}
"""
    else:
        return f"""Deduce the Semantic Constraints: You are given a Python program and its expected output. Find one input such that executing the program with the input leads to the given output. Complete the assertion with one such input in between [ANSWER] and [/ANSWER].
PYTHON]
{code}
assert f(??) == {output}
[/PYTHON]

{special_token}
"""
    