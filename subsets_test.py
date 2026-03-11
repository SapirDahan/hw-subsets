import pytest
import networkx as nx
from subsets import sorted_subset_sums
from testcases import parse_testcases

testcases = parse_testcases("testcases.txt")

def run_testcase(input:str):
    from itertools import takewhile, islice
    output = ""
    for i in eval(input):
        output += f"{i}, "
    output = output[:-2]  # remove last comma
    return output

@pytest.mark.parametrize("testcase", testcases, ids=[testcase["name"] for testcase in testcases])
def test_cases(testcase):
    actual_output = run_testcase(testcase["input"])
    assert actual_output == testcase["output"], f"Expected {testcase['output']}, got {actual_output}"


def test_new_cases():
    # your new tests here
    pass
