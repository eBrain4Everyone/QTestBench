import json
import pennylane as qml
import pennylane.numpy as np

symbols = ["H", "H", "H"]


def h3_ground_energy(bond_length):
    
    """
    Uses VQE to calculate the ground energy of the H3+ molecule with the given bond length.
    
    Args:
        - bond_length(float): The bond length of the H3+ molecule modelled as an
        equilateral triangle.
    Returns:
        - Union[float, np.tensor, np.array]: A float-like output containing the ground 
        state of the H3+ molecule with the given bond length.
    """
    


    coordinates = np.array([[0, 0, 0], [bond_length, 0, 0], [bond_length / 2, bond_length * np.sqrt(3) / 2, 0]])
    H, qubits = qml.qchem.molecular_hamiltonian(symbols, coordinates, charge=+1)
    print("Number of qubits = ", qubits)
    print("The Hamiltonian is ", H)

    electrons = 2
    hf = qml.qchem.hf_state(electrons, qubits)
    print(hf)

    dev = qml.device('default.qubit', wires=6)

    @qml.qnode(dev, interface="autograd")
    def circuit(params):
        x, y, z = params
        qml.BasisState(np.array([1, 1, 0, 0, 0, 0]), wires=[i for i in range(6)])
        qml.DoubleExcitation(x, wires=[0, 1, 2, 3])
        qml.DoubleExcitation(y, wires=[0, 1, 4, 5])
        qml.ctrl(qml.SingleExcitation, control=0)(z, wires=[1, 3])
        return qml.expval(H)


    opt = qml.GradientDescentOptimizer(stepsize=0.5)
    max_iterations = 1000
    convergence_threshold = 1e-06
    
    params = np.array([0.1, 0.2, 0.3])
    for i in range(max_iterations):
        old_cost = circuit(params)
        params = opt.step(circuit, params) 
        new_cost = circuit(params)
        print(f"Step = {i},  Cost function = {new_cost:.8f} ")
        if abs(new_cost-old_cost) < convergence_threshold:
            return new_cost


# These functions are responsible for testing the solution.

def run(test_case_input: str) -> str:
    ins = json.loads(test_case_input)
    outs = h3_ground_energy(ins)
    return str(outs)


def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(solution_output,expected_output, atol = 1e-4), "Not the correct ground energy"


# These are the public test cases
test_cases = [
    ('1.5', '-1.232574'),
    ('0.8', '-0.3770325')
]

# This will run the public test cases locally
for i, (input_, expected_output) in enumerate(test_cases):
    print(f"Running test case {i} with input '{input_}'...")

    try:
        output = run(input_)

    except Exception as exc:
        print(f"Runtime Error. {exc}")

    else:
        if message := check(output, expected_output):
            print(f"Wrong Answer. Have: '{output}'. Want: '{expected_output}'.")

        else:
            print("Correct!")