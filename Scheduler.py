import numpy as np
import ReadInFile
from Classes import State
from Classes import Country
import ResourceQuality
from random import randint
import math


def country_participation_probability(discounted_reward, x_0, k, L=1):
    return L / (1 + math.exp(-k * (discounted_reward - x_0)))


def schedule_probability(probability_for_countries):
    return np.product(probability_for_countries)


def expected_utility(probability, self_discounted_reward):
    return probability * self_discounted_reward


def a_star_search(graph, start_state, goal):
    # TODO: Implement A* search algorithm
    return 0


def depth_first_search(graph, start_state, goal):
    # TODO: Implement depth first search algorithm
    return 0


def breadth_first_search(graph, start_state, goal):
    # TODO: Implement breadth first search algorithm
    return 0


if __name__ == '__main__':
    country_dict = ReadInFile.getCountryDict()
    resource_dict = ReadInFile.getResourceDict()
    start_state = State(0, country_dict, [])
    my_country = country_dict["MyCountry"]
    # TODO: Test and Run Search
