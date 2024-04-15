from ..Model1.RandomGenerator import RandomGenerator
import csv


class SampleGenerator:
    def __init__(self, iterations):
        self.iterations = iterations
        self.samples = []

    __FILE_PATH = "../observations/samples.csv"

    def execute(self):
        self.__generate_samples(self.iterations)
        self.__save_samples_to_csv(self.__FILE_PATH)

    def __generate_samples(self, iterations):
        for _ in range(iterations):
            self.__generate_sample()

    def __generate_sample(self):
        norm_2_2_sample = RandomGenerator.getRand_Norm(2, 2)
        norm_2_15_sample = RandomGenerator.getRand_Norm(2, 1.5)
        norm_15_05_sample = RandomGenerator.getRand_Norm(1.5, 0.5)
        erl_sample = RandomGenerator.getRand_Erl(2, 3)
        self.samples.append(
            [norm_2_2_sample, norm_2_15_sample, norm_15_05_sample, erl_sample]
        )

    def __save_samples_to_csv(self, filename):
        print(self.samples)
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["rand_norm_2_2", "rand_norm_2_1.5", "rand_norm_1.5_0.5", "rand_erl"]
            )
            writer.writerows(self.samples)


generator = SampleGenerator(500)
generator.execute()
