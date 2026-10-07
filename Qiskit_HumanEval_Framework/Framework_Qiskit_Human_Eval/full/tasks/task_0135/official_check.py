def check(candidate):
    result = candidate()
    
    assert isinstance(result, NoiseModel), "Result should be a NoiseModel instance"
    
    global_error = result.to_dict()["errors"][0]['probabilities']
    assert global_error == [[0.98, 0.02], [0.03, 0.97]]
    
    qubit0_error = result.to_dict()["errors"][1]
    assert qubit0_error["gate_qubits"][0][0] == 0
    assert qubit0_error["probabilities"] == [[0.7, 0.3], [0.2, 0.8]]
    
    assert len(result.to_dict()["errors"]) == 2
