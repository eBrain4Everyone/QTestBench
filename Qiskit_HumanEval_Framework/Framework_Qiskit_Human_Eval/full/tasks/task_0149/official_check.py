def check(candidate):
    test_inputs = [
        {"001": 50, "101": 3},
        {"1": 1},
        {"01101": 302, "10010": 10, "101": 209},
    ]
    for counts in test_inputs:
        bit_array = BitArray.from_counts(counts)
        expected = max(counts.items(), key=lambda x: x[1])[0]
        assert candidate(bit_array) == expected
