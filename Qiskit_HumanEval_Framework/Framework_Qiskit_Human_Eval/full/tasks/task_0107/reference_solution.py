from qiskit.quantum_info import ScalarOp
def compose_scalar_ops() -> ScalarOp:
    """ Create two ScalarOp objects with dimension 2 and coefficient 2, compose them together, and return the resulting ScalarOp.
    """

    op1 = ScalarOp(2, 2)
    op2 = ScalarOp(2, 2)
    composed_op = op1.compose(op2)
    return composed_op
