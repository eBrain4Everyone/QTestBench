from qiskit_ibm_runtime.fake_provider import FakeCairoV2
from qiskit_aer.noise import NoiseModel
def gen_noise_model():
    """ Generate a noise model from the Fake Cairo V2 backend.
    """

    backend = FakeCairoV2()
    noise_model = NoiseModel.from_backend(backend)
    return noise_model
