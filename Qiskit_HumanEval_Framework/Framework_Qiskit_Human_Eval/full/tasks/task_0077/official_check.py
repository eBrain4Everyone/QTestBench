def check(candidate):
    from qiskit.quantum_info import Statevector
    def _check(input_dist):
        circuit = candidate(input_dist)
        # allow circuits with or without final measurements
        circuit.remove_final_measurements()
        probability_dist = Statevector(circuit).probabilities()
        for basis_state, target_probability in input_dist.items():
            assert math.isclose(
                target_probability, probability_dist[basis_state], abs_tol=0.05
            )

    for input_dist in [
        {0: 1},
        {0: 0.1, 1: 0.1, 2: 0.7, 3: 0.1},
        {0: 0.5, 3: 0.5},
        {1: 0.5, 2: 0.5},
    ]:
        _check(input_dist)
