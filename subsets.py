import bisect

def sorted_subset_sums(numbers):
    """
    Yields all subset sums of 'numbers', from smallest to largest.

    We use a sorted waiting list. Each entry holds two things:
        - the sum of a subset
        - which element was the last one added (so we know where to continue from)

    Each time we pop the smallest entry and yield its sum, we generate two follow-ups:

        EXTEND  — add the next element to the subset.
                  Example: we have {1, 2}, we extend by adding 4 → {1, 2, 4}

        REPLACE — drop the last element, put the next one in instead.
                  Example: we have {1, 2}, we replace 2 with 4 → {1, 4}

    These two moves together reach every possible subset exactly once.
    Since we always yield the smallest entry, the output comes out in order.

    Walkthrough for [1, 2, 4]:
        numbers = [1, 2, 4]   →   index 0=1,  index 1=2,  index 2=4

        yield 0                        ← empty subset, always first
        waiting: [({1}, sum=1)]        ← seed: only {1} to start with

        pop {1}, sum=1 → yield 1
            extend:  add numbers[1]=2  →  {1,2},  sum=3
            replace: swap 1 for numbers[1]=2  →  {2},  sum=2
        waiting: [({2}, sum=2),  ({1,2}, sum=3)]

        pop {2}, sum=2 → yield 2
            extend:  add numbers[2]=4  →  {2,4},  sum=6
            replace: swap 2 for numbers[2]=4  →  {4},  sum=4
        waiting: [({1,2}, sum=3),  ({4}, sum=4),  ({2,4}, sum=6)]

        pop {1,2}, sum=3 → yield 3
            extend:  add numbers[2]=4  →  {1,2,4},  sum=7
            replace: swap 2 for numbers[2]=4  →  {1,4},  sum=5
        waiting: [({4}, sum=4),  ({1,4}, sum=5),  ({2,4}, sum=6),  ({1,2,4}, sum=7)]

        index 2 is the last element — nothing left to extend or replace.
        yield 4, 5, 6, 7.

        output: 0, 1, 2, 3, 4, 5, 6, 7  as we wanted

    Examples:
        >>> # empty input — only the empty subset exists, so just 0
        >>> list(sorted_subset_sums([]))
        [0]

        >>> # single element — two subsets: {} and {7}
        >>> list(sorted_subset_sums([7]))
        [0, 7]

        >>> # input order doesn't matter, we sort internally
        >>> list(sorted_subset_sums([4, 1, 2]))
        [0, 1, 2, 3, 4, 5, 6, 7]

        >>> # duplicate sums are expected — both {3} and {1,2} sum to 3
        >>> list(sorted_subset_sums([1, 2, 3]))
        [0, 1, 2, 3, 3, 4, 5, 6]

        >>> list(sorted_subset_sums([1, 2, 4]))
        [0, 1, 2, 3, 4, 5, 6, 7]

        >>> list(sorted_subset_sums([1, 2, 3]))
        [0, 1, 2, 3, 3, 4, 5, 6]

        >>> list(sorted_subset_sums([2, 3, 4]))
        [0, 2, 3, 4, 5, 6, 7, 9]

        >>> from itertools import islice, takewhile
        >>> list(islice(sorted_subset_sums(range(100)), 5))
        [0, 0, 1, 1, 2]

        >>> list(takewhile(lambda x: x <= 6, sorted_subset_sums(range(1, 100))))
        [0, 1, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 6]

        >>> list(zip(range(5), sorted_subset_sums(range(100))))
        [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2)]

        >>> len(list(takewhile(lambda x:x<=1000, sorted_subset_sums(list(range(90,100)) + list(range(920,1000))))))
        1104

    """
    # sorting is required — the algorithm only works correctly if elements are in order
    numbers = sorted(numbers)
    n = len(numbers)

    yield 0  # the empty subset always has sum 0

    if n == 0:
        return

    # start with just the first element (the smallest possible non-empty subset)
    candidates = [(numbers[0], 0)]

    while candidates:
        s, i = candidates.pop(0)  # always take the smallest candidate from the front
        yield s

        if i + 1 < n:
            # extend: keep the current subset and also include the next element
            bisect.insort(candidates, (s + numbers[i + 1], i + 1))

            # replace: remove the last element and put the next one in its place instead
            bisect.insort(candidates, (s - numbers[i] + numbers[i + 1], i + 1))


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())