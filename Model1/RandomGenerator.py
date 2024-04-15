import math
import random


class RandomGenerator:
    @staticmethod
    def uniform_random():
        return random.uniform(0, 1)

    @staticmethod
    def getRand_Erl(k, theta):
        u_product = 1.0
        for _ in range(k):
            u_product *= RandomGenerator.uniform_random()
        return -theta * math.log(u_product)

    @staticmethod
    def getRand_Norm(mu, sigma):
        u1 = RandomGenerator.uniform_random()
        u2 = RandomGenerator.uniform_random()
        z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2 * math.pi * u2)
        return z0 * sigma + mu
