import importlib
import inspect
from qiskit_ibm_runtime.fake_provider import fake_backend
def fake_providers_v2_with_ecr() -> list:
    """ Return the list of names of all the fake providers of type FakeBackendV2 which contains ecr gates in its available operations.
    """

    fake_provider_module = importlib.import_module("qiskit_ibm_runtime.fake_provider")
    fake_providers = {}
    for name, obj in inspect.getmembers(fake_provider_module):
        if inspect.isclass(obj) and issubclass(obj, fake_backend.FakeBackendV2):
            fake_providers[name] = obj
    fake_providers_ecr = []
    for name, provider in fake_providers.items():
        backend = provider()
        if "ecr" in backend.operation_names:
            fake_providers_ecr.append(name)
    return fake_providers_ecr
