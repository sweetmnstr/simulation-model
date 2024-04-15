from __future__ import annotations
from abc import ABC, abstractmethod


import pandas as pd
from scipy.stats import kstest, chi2_contingency
import numpy as np
import matplotlib.pyplot as plt


class AbstractAnalizationCreator(ABC):
    @abstractmethod
    def create(self):
        pass


class ErlangAnalizationCreator(AbstractAnalizationCreator):
    def create(self, mean, std_deviation, sample_size, column_name) -> Statistic:
        return ErlangAnalization(mean, std_deviation, sample_size, column_name)


class NormalAnalizationCreator(AbstractAnalizationCreator):
    def create(self, mean, std_deviation, sample_size, column_name) -> Statistic:
        return NormalAnalization(mean, std_deviation, sample_size, column_name)


class Statistic(ABC):
    _df = pd.read_csv("../observations/samples.csv")

    def __init__(self, mean, std_deviation, sample_size, column_name):
        self._mean = mean
        self._std_deviation = std_deviation
        self._sample_size = sample_size
        self._column_name = column_name
        super().__init__()

    def execute(self) -> str:
        ks_p_value, ks_statistic = self._perform_ks_test()
        chi2, p, dof, expected_frequencies = self._perform_chi2_test()
        self.__create_histograms(
            self._df[self._column_name],
            expected_frequencies,
        )
        return self.__result_mapper(ks_p_value, ks_statistic, chi2, p, dof)

    def __create_histograms(self, sample, control_sample):
        # # Histogram of control data from CSV
        self.__create_histogram(
            control_sample, "Histogram of control", "Value", "Frequency", color="blue"
        )
        # # Histogram of sample data from CSV
        self.__create_histogram(
            self._df[self._column_name],
            "Histogram of sample",
            "Value",
            "Frequency",
            color="grey",
        )
        self.__create_comparation_histogram(control_sample, sample)

    def __create_histogram(
        self, data, title, xlabel, ylabel, color="blue", alpha=0.7, bins="auto"
    ):
        plt.hist(data, bins=bins, color=color, alpha=alpha, edgecolor="black")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    def __create_comparation_histogram(self, control_sample, sample_data):
        plt.hist(
            control_sample,
            bins="auto",
            color="blue",
            alpha=0.5,
            label="Control",
            edgecolor="black",
        )
        plt.hist(
            sample_data,
            bins="auto",
            color="red",
            alpha=0.5,
            label="Sample",
            edgecolor="black",
        )
        plt.title("Comparison of Control and Sample Histograms")
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.legend(loc="upper right")
        plt.show()

    def __result_mapper(self, ks_p_value, ks_statistic, chi2, p, dof) -> str:
        return f"Ks p-value: {ks_p_value}\nKs statistic: {ks_statistic}\nChi2 result: {chi2}\nChi2 dof: {dof}\nChi2 p-value: {p}"

    @abstractmethod
    def _perform_ks_test(self):
        pass

    @abstractmethod
    def _perform_chi2_test(self):
        pass


class ErlangAnalization(Statistic):
    def _perform_ks_test(self):
        return kstest(
            self._df[self._column_name],
            "gamma",
            args=(self._mean, 0, self._std_deviation),
        )

    def _perform_chi2_test(self):
        observed_frequencies = self._df[self._column_name]
        expected_frequencies = np.random.gamma(
            self._mean, self._std_deviation, self._sample_size
        )
        chi2, p, dof, _ = chi2_contingency([observed_frequencies, expected_frequencies])
        return chi2, p, dof, expected_frequencies


class NormalAnalization(Statistic):
    def _perform_ks_test(self):
        return kstest(
            self._df[self._column_name], "norm", args=(self._mean, self._std_deviation)
        )

    def _perform_chi2_test(self):
        observed_frequencies = np.abs(self._df[self._column_name])
        expected_frequencies = np.abs(
            np.random.normal(self._mean, self._std_deviation, self._sample_size)
        )
        chi2, p, dof, _ = chi2_contingency([observed_frequencies, expected_frequencies])
        return chi2, p, dof, expected_frequencies


def printResults(analizations):
    for analization in analizations:
        print(analization.execute())


erlang_creator = ErlangAnalizationCreator()
normal_creator = NormalAnalizationCreator()
erlang_analization = erlang_creator.create(2, 3, 500, "rand_erl")
normal_2_2_analization = normal_creator.create(2, 2, 500, "rand_norm_2_2")
normal_2_15_analization = normal_creator.create(2, 1.5, 500, "rand_norm_2_1.5")
normal_15_05_analization = normal_creator.create(1.5, 0.5, 500, "rand_norm_1.5_0.5")

# printResults(
#     [
#         erlang_analization,
#         normal_2_2_analization,
#         normal_2_15_analization,
#         normal_15_05_analization,
#     ]
# )

print(normal_2_2_analization.execute())
