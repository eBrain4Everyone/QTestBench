def check(candidate):
    backend_can = candidate()
    assert backend_can == "fake_auckland" or "auckland" in backend_can
