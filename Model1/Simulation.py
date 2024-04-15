import csv
from .Server import Server
from .RandomGenerator import RandomGenerator
from .Job import Job
from .LIFOQueue import LIFOQueue


class Simulation:
    __FILE_PATH = "../observations/simulation_results.csv"

    def __init__(self):
        self.current_time = 0
        self.modeling_time = 500
        self.server = Server()
        self.queue = LIFOQueue()
        self.next_job1_time = RandomGenerator.getRand_Erl(2, 3)
        self.next_job2_time = RandomGenerator.getRand_Norm(2, 2)
        self.service_completion_time = 501
        self.process_table = []
        self.max_queue_length = 0
        self.downtime = 0

    def run(self):
        while self.current_time < self.modeling_time:
            # Determine the next event
            next_event_time = min(
                self.next_job1_time, self.next_job2_time, self.service_completion_time
            )

            # Update downtime
            if self.server.status == 0 and self.current_time < next_event_time:
                self.downtime += next_event_time - self.current_time

            # Update current time
            self.current_time = next_event_time

            # Arrival of job type 1
            if self.current_time == self.next_job1_time:
                job = Job("J1")
                self.__handle_arrival(job)
                self.next_job1_time += RandomGenerator.getRand_Erl(2, 3)

            # Arrival of job type 2
            elif self.current_time == self.next_job2_time:
                job = Job("J2")
                self.__handle_arrival(job)
                self.next_job2_time += RandomGenerator.getRand_Norm(2, 2)

            # Service completion
            elif self.current_time == self.service_completion_time:
                self.__handle_service_completion()

            # Record the state
            self.__record_state()

            # Update max queue length
            self.max_queue_length = max(self.max_queue_length, self.queue.length())

        # Output the results
        self.__output_results()

    def __handle_arrival(self, job):
        if self.server.status == 0:
            self.service_completion_time = self.server.start_processing(
                job, self.current_time
            )
        else:
            self.queue.add(job)

    def __handle_service_completion(self):
        self.server.finish_processing()
        if not self.queue.is_empty():
            next_job = self.queue.get()
            self.service_completion_time = self.server.start_processing(
                next_job, self.current_time
            )
        else:
            self.service_completion_time = 501

    def __record_state(self):
        self.process_table.append(
            {
                "Event #": len(self.process_table),
                "Current Time": self.current_time,
                "J1 Arrival": self.next_job1_time,
                "J2 Arrival": self.next_job2_time,
                "Service Completion": self.service_completion_time,
                "Server Status": self.server.status,
                "Queue Length": self.queue.length(),
                "Queue Content": self.queue.__repr__(),
            }
        )

    def __output_results(self):
        MoE1 = self.downtime / self.modeling_time
        MoE2 = self.max_queue_length
        print(f"Downtime factor (MoE1): {MoE1}")
        print(f"Max. of all jobs in queue (MoE2): {MoE2}")

        # Output the process table to a CSV file
        with open(self.__FILE_PATH, "w", newline="") as csvfile:
            fieldnames = [
                "Event #",
                "Current Time",
                "J1 Arrival",
                "J2 Arrival",
                "Service Completion",
                "Server Status",
                "Queue Length",
                "Queue Content",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.process_table:
                writer.writerow(row)
