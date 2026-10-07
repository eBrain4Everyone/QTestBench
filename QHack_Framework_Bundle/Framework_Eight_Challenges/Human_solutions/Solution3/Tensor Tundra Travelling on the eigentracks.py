import json
import pennylane as qml
import pennylane.numpy as np
import scipy

H = np.array([[ 0.39488016,  0.04722628, -0.17943126, -0.03673282],
        [ 0.04722628,  0.37758558,  0.12997088,  0.17848188],
        [-0.17943126,  0.12997088,  0.53582574,  0.01115543],
        [-0.03673282,  0.17848188,  0.01115543,  0.29170851]])


U = scipy.linalg.expm(2 * np.pi * 1j * H) 


def state_prep(params, wires):

    """
    Implements the state preparation circuit.

    Args:
        - params (np.array(float)): Angles [theta_1, theta_2, theta_3] parametrizing
        the RY rotations in the circuit.
        - wires (list): Labels for the circuit wires.
    Returns:
        - Does not return anything since it is a subcircuit.
    """
    


    # Put your code here
    qml.RY(params[0], wires = wires[0])
    qml.RY(params[1], wires =  wires[1])
    qml.CNOT(wires = [wires[0], wires[1]] )
    qml.RY(params[2],wires = wires[1])


dev = qml.device('lightning.qubit', wires = range(8))
 
@qml.qnode(dev)
def qpe_circuit(params):

    """
    Implements the QPE routine for the Unitary U, including initial state 
    preparation using the state_prep subcircuit.

    Args:
        - params (np.array(float)): Angles [theta_1, theta_2, theta_3] parametrizing
        the RY rotations in the state_prep circuit.
    Returns:
        - np.tensor(float): Computational basis probabilities in the estimation wires.
    """
    


    # Put your code here
    wires = list(range(8))
    target = wires[-2:]
    estimation_wires = wires[:-2]
    
    state_prep(params, wires=target)
    qml.QuantumPhaseEstimation(U, target_wires=target, estimation_wires=estimation_wires)
    return qml.probs(wires=estimation_wires)


def compute_statistics(params):

    """
    Computes the phase and its uncertainty by postprocessing the results of the QPE circuit.

    Args:
        - params (np.array(float)): Angles [theta_1, theta_2, theta_3] parametrizing
        the RY rotations in the state_prep circuit.
    Returns:
        - mu (float): The phase calculated as a weighted average.
        - sigma (float): The uncertainty calculated as the standard deviation
        for the phase.
    """

    # Put your code here #
    probs = qpe_circuit(params)
    phases = np.array(list(range(len(probs)))) / (2**6)
    
    mu = np.sum(probs*phases).numpy() # mean
    sigma = np.sqrt(np.sum(probs*(phases-mu)**2)).numpy() # standard deviation

    return mu, sigma


# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    ins = np.array(json.loads(test_case_input))
    outs = list(compute_statistics(ins))
    
    return str(outs)


def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)

    assert np.allclose(solution_output, expected_output, atol = 1e-4)


# These are the public test cases
test_cases = [
    ('[1.35889209, -0.6219561, -1.31577162]', '[0.121662, 0.120539]'),
    ('[4.40084815, -0.77288063,  0.6425846]', '[0.303264, 0.043692]')
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