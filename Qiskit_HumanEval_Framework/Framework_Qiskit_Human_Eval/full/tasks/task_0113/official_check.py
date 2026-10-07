def check(candidate):
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.barrier()
    qc.cx(0, 1)
    qc.barrier()
    qc.cx(1, 2)
    qc.measure_all()
    
    property_set = candidate(qc)
    
    assert property_set["depth_before"] == qc.depth(), "'depth_before' should match the original circuit depth"
    assert property_set["width"] == qc.width(), "'width' should match the circuit width"
    optimized_qc = PassManager(RemoveBarriers()).run(qc)
    assert property_set["depth_after"] == optimized_qc.depth(), "'depth_after' should match the depth of a barrier-free circuit"
