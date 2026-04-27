import pytest
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
    # Empty input — only valid subset is the empty set, so the only sum is 0
    assert list(sorted_subset_sums([])) == [0]

    # Single element — two subsets: {} with sum 0, and {5} with sum 5
    assert list(sorted_subset_sums([5])) == [0, 5]

    # Check that the output is actually sorted (not just correct values)
    result = list(sorted_subset_sums([3, 7, 1]))
    assert result == sorted(result), "output should be in ascending order"

    # The number of results must be 2^n — one for each possible subset
    for n in range(1, 6):
        numbers = list(range(1, n + 1))   # [1], [1,2], [1,2,3], ...
        assert len(list(sorted_subset_sums(numbers))) == 2 ** n

    # The number of results must be 2^n — one for each possible subset
    for n in range(1, 15):
        numbers = list(range(1, n + 1))  # [1], [1,2], [1,2,3], ...
        assert len(list(sorted_subset_sums(numbers))) == 2 ** n

    # Make sure we actually get the right total count for a set with duplicates in sums.
    # [1, 2, 3] has 8 subsets: {}, {1}, {2}, {3}, {1,2}, {1,3}, {2,3}, {1,2,3}
    # sums: 0, 1, 2, 3, 3, 4, 5, 6
    assert list(sorted_subset_sums([1, 2, 3])) == [0, 1, 2, 3, 3, 4, 5, 6]

    # Order of input shouldn't matter — we sort internally
    assert list(sorted_subset_sums([3, 1, 2])) == list(sorted_subset_sums([1, 2, 3]))

    # Large gaps between numbers
    assert list(sorted_subset_sums([1, 100])) == [0, 1, 100, 101]

    # takewhile stops as soon as a value exceeds 3 — the generator should never
    # compute the rest. this confirms it's truly lazy and not building a full list.
    from itertools import takewhile
    result = list(takewhile(lambda x: x <= 3, sorted_subset_sums([1, 2, 3, 4, 5])))
    assert result == [0, 1, 2, 3, 3]

    # same idea but on a huge input — range(1000000) has 2^1000000 possible subsets,
    # so there's no way this works unless the generator is truly lazy.
    # we only ask for sums up to 5, so it should finish instantly.
    result = list(takewhile(lambda x: x <= 5, sorted_subset_sums(range(1000000))))
    assert result == [0, 0, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5]

    from itertools import islice
    # islice grabs exactly the first N results and stops — another way to use the generator lazily
    result = list(islice(sorted_subset_sums([5, 10, 15, 20]), 4))
    assert result == [0, 5, 10, 15]

    # zip stops when the shorter side (range(4)) runs out — so we only get 4 subset sums
    result = list(zip(range(4), sorted_subset_sums([5, 10, 15, 20])))
    assert result == [(0, 0), (1, 5), (2, 10), (3, 15)]

    # count how many subset sums of [1,2,3,4,5] are <= 10
    count = len(list(takewhile(lambda x: x <= 10, sorted_subset_sums([1, 2, 3, 4, 5]))))
    assert count == 25
