def check(candidate):
    from qiskit.quantum_info import random_statevector
    rs = random_statevector(dims = 16)
    qargs = [0,1]
    schmidt_decomp = candidate(rs, qargs)
    for _, item in enumerate(schmidt_decomp):
        assert item[0]>=0, "Schmidt coefficients must be real"
        assert item[1].dims() == (2,2), "The dimension of the first subsystem doesn't match"
        assert item[2].dims() == (2,2), "The dimension of the second subsystem doesn't match"
