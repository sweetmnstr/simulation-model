from .RandomGenerator import RandomGenerator


class Job:
    def __init__(self, job_type):
        self.job_type = job_type
        self.processing_time = self.set_processing_time()

    def set_processing_time(self):
        if self.job_type == "J1":
            return RandomGenerator.getRand_Norm(2, 1.5)
        elif self.job_type == "J2":
            return RandomGenerator.getRand_Norm(1.5, 0.5)
        return None
