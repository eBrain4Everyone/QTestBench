import datetime
from qiskit_ibm_runtime import QiskitRuntimeService
def find_recent_jobs():
    """ Find and return jobs submitted in the last three months using QiskitRuntimeService.
    """

    three_months_ago = datetime.datetime.now() - datetime.timedelta(days=90)
    service = QiskitRuntimeService()
    jobs_in_last_three_months = service.jobs(created_after=three_months_ago)
    return jobs_in_last_three_months
