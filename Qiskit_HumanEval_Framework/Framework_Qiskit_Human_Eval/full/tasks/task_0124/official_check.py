def check(candidate):
    backend = FakeCairoV2()
    expected_nm = NoiseModel.from_backend(backend)
    noise_model = candidate()
    assert type(noise_model) == NoiseModel
    assert noise_model == expected_nm
