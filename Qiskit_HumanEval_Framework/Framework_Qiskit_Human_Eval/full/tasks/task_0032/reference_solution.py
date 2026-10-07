from numpy import float64
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Estimator
from qiskit.quantum_info import SparsePauliOp
def estimator_qiskit() -> float64:
    """ Run a Bell circuit on Qiskit Estimator and return expectation values for the bases II, XX, YY, ZZ.
    """

    observable = SparsePauliOp(["II","XX","YY","ZZ"], coeffs=[1, 1, -1, 1])
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0,1)

    estimator = Estimator(mode=AerSimulator())
    job = estimator.run([(qc, observable)])
    result = job.result()[0].data.evs.item()
    return result
