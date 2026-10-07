def check(candidate):
    from qiskit.quantum_info import Statevector
    from math import sqrt
    candidate()
    with open('bell.qpy', 'rb') as fd:
        data = qpy.load(fd)[0]
    bell_state = (Statevector.from_label("11") + Statevector.from_label("00"))/sqrt(2)
    assert Statevector.from_instruction(data) == bell_state
