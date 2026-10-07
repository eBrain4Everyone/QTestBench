def check(candidate):
    from qiskit.circuit.library import XGate, HGate
    from qiskit_aer import AerSimulator
    from qiskit_ibm_runtime import Sampler
    from qiskit.result import marginal_distribution
    result_x = candidate([XGate()])
    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    assert isinstance(result_x, QuantumCircuit)
    assert result_x.num_qubits == 3
    assert result_x.count_ops()['x'] == 1 and result_x.count_ops()['if_else'] == 2
    assert  marginal_distribution(sampler.run([result_x]).result()[0].data.c_receiver.get_counts()) == {'1': 1024}
    result_h = candidate([HGate()])
    assert result_h.count_ops()['h'] == 3 and result_h.count_ops()['if_else'] == 2
    assert round(marginal_distribution(sampler.run([result_h]).result()[0].data.c_receiver.get_counts())['0']/1024, 1) == 0.5
