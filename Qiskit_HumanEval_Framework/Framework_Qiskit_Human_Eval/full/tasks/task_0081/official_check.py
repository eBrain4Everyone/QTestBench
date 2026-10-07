def check(candidate):
    from qiskit.quantum_info import Statevector
    from math import sqrt
    data = candidate()
    bell_state = (Statevector.from_label("11") + Statevector.from_label("00"))/sqrt(2)
    assert Statevector.from_instruction(data) == bell_state
