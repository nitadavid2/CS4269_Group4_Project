import numpy as np
import ReadInFile
from Classes import State
from Classes import Country
import ResourceQuality
import math
import queue


def schedule_probability(probability_for_countries):
    return np.product(probability_for_countries)


def expected_utility(probability, self_discounted_reward):
    return probability * self_discounted_reward


def a_star_search(start, depth, utility):
    # TODO: Implement A* search algorithm

    # We will use a priority queue for the A* implementation.
    # We will expand the frontier each time by expanding the "best path" using the
    # (expected utility - utility) as heuristic.
    search_queue = queue.PriorityQueue()

    # We will have a queue of possible, valid paths
    solution_queue = queue.PriorityQueue()

    # A "schedule" is defined as list of actions (transfers or transforms)
    # Query the .path attribute of a state for path to current state.
    # Query .countries for states of countries currently in state.
    # Query .depth to get current depth

    # Initialize search_queue
    for suc in start.findSuccessor():
        util = suc.discounted_reward()  # TODO: Fix
        # Use -util since PriorityQueue.get() takes item with lowest priority
        search_queue.put((-util, suc))

    # Explore search_queue
    while search_queue.not_empty:
        next_item = search_queue.get()
        next_state_value, next_state = next_item[0], next_item[1]

        # Push current state to queue storing possible solutions
        solution_queue.put(next_item)

        # Before we go on, check current depth
        if next_state.depth < depth:
            # Now generate successors
            for suc in next_state.findSuccessor():
                util = suc.discounted_reward()  # TODO: Fix
                search_queue.put((-util, suc))

    # Return best option
    answer_item = solution_queue.get()
    answer_value = -answer_item[0]
    answer_path = answer_item[1]

    # TODO: Remove after testing.
    print(answer_value)
    print(answer_path)

    return answer_path


def depth_first_search(start, depth, utility):
    # TODO: Implement depth first search algorithm
    return 0


def breadth_first_search(start, depth, utility):
    # TODO: Implement breadth first search algorithm
    return 0


if __name__ == '__main__':
    country_dict = ReadInFile.getCountryDict()
    resource_dict = ReadInFile.getResourceDict()
    start_state = State(0, country_dict, [])
    my_country = country_dict['MyCountry']
    # TODO: Test and Run Search

    test = a_star_search(start_state, 1, 1)
    print(test)
