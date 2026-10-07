def check(candidate):
    from qiskit.quantum_info import Statevector
    import math
    import matplotlib

    def check_circuit(circuit):
        assert circuit.data[-1].operation.name == "measure"
        circuit.remove_final_measurements()
        ghz_statevector = (
            Statevector.from_label("000") + Statevector.from_label("111")
        ) / math.sqrt(2)
        assert Statevector.from_instruction(circuit).equiv(ghz_statevector)

    circuit = candidate()
    check_circuit(circuit)

    circuit, drawing = candidate(drawing=True)
    check_circuit(circuit)
    assert isinstance(drawing, matplotlib.figure.Figure)
