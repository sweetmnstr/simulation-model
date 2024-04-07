class Server:
    def __init__(self):
        self.status = 0  # 0 - free, 1 - busy
        self.job = None

    def start_processing(self, job, current_time):
        self.status = 1
        self.job = job
        return current_time + job.processing_time

    def finish_processing(self):
        self.status = 0
        self.job = None
