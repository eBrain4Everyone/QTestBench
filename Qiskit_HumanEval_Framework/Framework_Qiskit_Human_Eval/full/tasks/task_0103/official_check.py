def check(candidate):
    providers_can = candidate()
    providers_exp = [
        "FakeCusco",
        "FakeKawasaki",
        "FakeKyiv",
        "FakeKyoto",
        "FakeOsaka",
        "FakePeekskill",
        "FakeQuebec",
        "FakeSherbrooke",
        "FakeBrisbane",
        "FakeCairoV2",
    ]
    for providers in providers_can:
        assert providers in providers_exp
    for providers in providers_exp:
        assert providers in providers_can
