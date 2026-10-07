import numpy as np
def check(candidate):
    # Check output structure
    result_live = candidate(True)
    result_dud = candidate(False)
    assert isinstance(result_live, tuple) and len(result_live) == 3, "Output format incorrect"
    assert isinstance(result_dud, tuple) and len(result_dud) == 3, "Output format incorrect"

    # Live bomb case (probabilities should sum to ~1)
    assert 0.85 <= result_live[0] <= 1.0, "Live bomb predictions should be high"
    assert 0.0 <= result_live[1] <= 0.05, "Dud predictions should be minimal"
    assert 0.0 <= result_live[2] <= 0.15, "Detonations should be low"
    # Dud bomb case
    assert np.isclose(result_dud, (0.0, 1.0, 0.0), atol=0.01).all(), "Dud bomb should always return (0.0, 1.0, 0.0)"
    # Consistency check (running multiple times should yield similar results)
    results = [candidate(True) for _ in range(5)]
    means = np.mean(results, axis=0)
    assert 0.85 <= means[0] <= 1.0, "Average live prediction should be high"
    assert 0.0 <= means[1] <= 0.05, "Average dud prediction should be minimal"
    assert 0.0 <= means[2] <= 0.15, "Average detonation rate should be low"
    print("All tests passed successfully!")
