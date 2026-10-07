def check(candidate):
    assert candidate().num_parameters >= 2 , "The circuit doesn't cover the bloch sphere."
    assert candidate().num_parameters <= 5 , "The circuit is too long"
