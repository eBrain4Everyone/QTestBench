from qiskit.quantum_info import random_statevector, state_fidelity, Statevector
def fidelity_dataset():
    """ Return a list of ten pairs of one qubit state vectors whose state fidelity is greater than 0.9.
    """

    fidelity_dataset_list = []
    while len(fidelity_dataset_list)<=9:
        sv_1 = random_statevector(2)
        sv_2 = random_statevector(2)
        if state_fidelity(sv_1, sv_2) >= 0.9:
            fidelity_dataset_list.append((sv_1,sv_2))
    return fidelity_dataset_list
