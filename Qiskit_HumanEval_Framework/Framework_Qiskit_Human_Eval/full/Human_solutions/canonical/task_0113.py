from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager, PropertySet
from qiskit.transpiler.passes import RemoveBarriers
def calculate_depth_after_barrier_removal(qc: QuantumCircuit) -> PropertySet:
    """ Remove barriers from the given quantum circuit and calculate the depth before and after removal.
    Return a PropertySet with 'depth_before', 'depth_after', and 'width' properties.
    The function should only remove barriers and not perform any other optimizations.
    """

    property_set = PropertySet()
    property_set["depth_before"] = qc.depth()
    property_set["width"] = qc.width()
    
    pass_manager = PassManager(RemoveBarriers())
    optimized_qc = pass_manager.run(qc)
    
    property_set['depth_after'] = optimized_qc.depth()
    
    return property_set
