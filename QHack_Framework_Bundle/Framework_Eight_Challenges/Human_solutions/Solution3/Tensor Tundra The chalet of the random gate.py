import json
import pennylane as qml
import pennylane.numpy as np

# Define your device

dev = qml.device("default.mixed", wires=1)


@qml.qnode(dev)
def random_gate(p,q,r):

    """
    Applies a Pauli X, Pauli Y, Pauli Z or does nothing at random.

    Args:
        - p (float): probability of applying Pauli X.
        - q (float): probability of applying Pauli Y.
        - r (float): probability of applying Pauli Z.

    Returns:
        - (np.tensor(float)): Measurement probabilities in the computational basis.

    """
    qml.BitFlip(p+q, wires=0)
    return qml.probs(wires=[0])
    # Put your code here
    


# These functions are responsible for testing the solution.


def run(test_case_input: str) -> str:
    ins = np.array(json.loads(test_case_input))
    outs = random_gate(*ins).tolist()
    return str(outs)


def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)

    assert np.allclose(solution_output, expected_output, rtol = 1e-4), "Not the correct probabilities"


# These are the public test cases
test_cases = [
    ('[0.25, 0.25, 0.25]', '[0.5, 0.5]'),
    ('[0.125, 0.25, 0.2]', '[0.625, 0.375]')
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