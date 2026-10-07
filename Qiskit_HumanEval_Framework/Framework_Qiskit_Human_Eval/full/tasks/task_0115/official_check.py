def check(candidate):
    target = candidate()
    assert isinstance(target, Target)

    instructions = target.instructions
    u_gate_instructions = [inst for inst in instructions if inst[0].name == "u"]
    cx_gate_instructions = [inst for inst in instructions if inst[0].name == 'cx']

    assert len(u_gate_instructions) == 2
    assert len(cx_gate_instructions) == 2

    for inst in u_gate_instructions + cx_gate_instructions:
        props = target[inst[0].name][inst[1]]
        assert isinstance(props, InstructionProperties)
        assert props.duration > 0
        assert props.error >= 0

    assert set(inst[1] for inst in u_gate_instructions) == {(0,), (1,)}
    assert set(inst[1] for inst in cx_gate_instructions) == {(0, 1), (1, 0)}
