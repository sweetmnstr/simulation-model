class LIFOQueue:
    def __init__(self):
        self.queue = []

    def add(self, job):
        self.queue.append(job)

    def get(self):
        return self.queue.pop() if self.queue else None

    def is_empty(self):
        return len(self.queue) == 0

    def length(self):
        return len(self.queue)

    def __repr__(self):
        return str([job.job_type for job in self.queue])
