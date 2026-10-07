def check(candidate):
    from qiskit_aer import AerSimulator
    from qiskit_ibm_runtime import Sampler, SamplerOptions
    from qiskit_ibm_runtime.options import SamplerOptions
    circ_res = candidate()
    assert type(circ_res) == QuantumCircuit 
    assert circ_res.num_qubits == 4
    assert circ_res.num_clbits == 4
    assert any(instr.operation.name == "if_else" and instr.operation.num_qubits == 1 and instr.operation.num_clbits == 3 for instr in circ_res.data)
    
    sim = AerSimulator()
    options = SamplerOptions()
    options.simulator.seed_simulator=17
    sampler = Sampler(mode=sim, options=options)
    counts = sampler.run([circ_res], shots=1024).result()[0].data.c.get_counts()
    for outcome, _ in counts.items():
        qubit_states = outcome[::-1]
        q3_state = int(qubit_states[3])
        q0 = int(qubit_states[0])
        q1 = int(qubit_states[1])
        q2 = int(qubit_states[2])
        expected_q3_state = (q0 ^ q1 ^ q2)
        assert q3_state == expected_q3_state
