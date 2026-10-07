from qiskit.circuit import Parameter, QuantumCircuit

def remove_unassigned_parameterized_gates(circuit: QuantumCircuit) -> QuantumCircuit:
    """ Remove all the gates with unassigned parameters from the given circuit.
    """

    circuit_data = circuit.data.copy()
    circuit_without_params = QuantumCircuit(circuit.num_qubits, circuit.num_clbits)
    
    #for instr, qargs, cargs in circuit_data:
    for instruction in circuit_data:
        instr, qargs, cargs = instruction.operation, instruction.qubits, instruction.clbits
        if not (len(instr.params) > 0 and isinstance(instr.params[0], Parameter)):
            circuit_without_params.append(instr, qargs, cargs)

    return circuit_without_params
