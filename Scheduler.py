import numpy as np
import ReadInFile
from Classes import State
from Classes import Country
import ResourceQuality
import math
import queue
import time
import multiprocessing
from functools import partial


def schedule_probability(probability_for_countries):
    return np.product(probability_for_countries)


def expected_utility(probability, self_discounted_reward):
    return probability * self_discounted_reward


def mp_a_star_search(start, depth):
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
        # Get schedule probability
        country_probs = [c.participation_prob for c in suc.countries.values()]
        total_prob = schedule_probability(country_probs)

        # Get discounted reward of MyCountry
        dr = suc.countries['MyCountry'].discounted_reward

        # Calculate E.U.
        eu = expected_utility(total_prob, dr)

        # Use -util since PriorityQueue.get() takes item with lowest priority
        search_queue.put((-eu, suc))

    # Explore search_queue
    while search_queue.qsize() > 0:
        next_item = search_queue.get()
        next_state_value, next_state = next_item[0], next_item[1]

        # Push current state to queue storing possible solutions
        solution_queue.put(next_item)

        # Trim solution queue to size of about 100 when it grows too big
        if solution_queue.qsize() > 5000:
            print("Trim Solution queue")
            swap_queue = queue.PriorityQueue()
            for i in range(50):
                swap_queue.put(solution_queue.get())
            solution_queue = swap_queue

        # Before we go on, check current depth
        if next_state.depth < depth:
            # Now generate successors
            successors = next_state.findSuccessor()
            for suc in next_state.findSuccessor():
                # Get schedule probability
                country_probs = [c.participation_prob for c in suc.countries.values()]
                total_prob = schedule_probability(country_probs)

                # Get discounted reward of MyCountry
                dr = suc.countries['MyCountry'].discounted_reward

                # Calculate E.U.
                eu = expected_utility(total_prob, dr)

                # Add to queue
                search_queue.put((-eu, suc))

    # Return best option
    answer_item = solution_queue.get()
    answer_value = -answer_item[0]
    answer_path = answer_item[1].path

    # TODO: Remove after testing.
    print("Number of solutions: ", solution_queue.qsize())
    print("Best solution EU: ", answer_value)
    print("Best Path: ", answer_path)

    return answer_path

def a_star_search(start, depth):
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
        # Get schedule probability
        country_probs = [c.participation_prob for c in suc.countries.values() if c.participation_prob != -1]
        # print(country_probs)
        total_prob = schedule_probability(country_probs)

        # Get discounted reward of MyCountry
        dr = suc.countries['MyCountry'].discounted_reward

        # Calculate E.U.
        eu = expected_utility(total_prob, dr)

        # Use -util since PriorityQueue.get() takes item with lowest priority
        search_queue.put((-eu, suc))

    # Explore search_queue
    while search_queue.qsize() > 0:
        next_item = search_queue.get()
        next_state_value, next_state = next_item[0], next_item[1]

        # Push current state to queue storing possible solutions
        solution_queue.put(next_item)

        # Trim solution queue to size of about 100 when it grows too big
        if solution_queue.qsize() > 5000:
            # Return best option
            answer_item = solution_queue.get()
            answer_value = -answer_item[0]
            answer_path = answer_item[1].path

            # TODO: Remove after testing.
            print("Number of solutions: ", solution_queue.qsize())
            print("Best solution EU: ", answer_value)
            print("Best Path: ", answer_path)

            return answer_path

            print("Trim Solution queue")
            swap_queue = queue.PriorityQueue()
            for i in range(50):
                swap_queue.put(solution_queue.get())
            solution_queue = swap_queue

        # Before we go on, check current depth
        if next_state.depth < depth:
            # Now generate successors
            for suc in next_state.findSuccessor():
                # Get schedule probability
                country_probs = [c.participation_prob for c in suc.countries.values()]
                total_prob = schedule_probability(country_probs)

                # Get discounted reward of MyCountry
                dr = suc.countries['MyCountry'].discounted_reward

                # Calculate E.U.
                eu = expected_utility(total_prob, dr)

                # Add to queue
                search_queue.put((-eu, suc))

    # Return best option
    answer_item = solution_queue.get()
    answer_value = -answer_item[0]
    answer_path = answer_item[1].path

    # TODO: Remove after testing.
    print("Number of solutions: ", solution_queue.qsize())
    print("Best solution EU: ", answer_value)
    print("Best Path: ", answer_path)

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
    start = time.perf_counter()
    # pool = multiprocessing.Pool(processes=4)
    # prod_x = partial(a_star_search, depth=2)
    # test = pool.map(prod_x, (start_state,))
    test = a_star_search(start_state, 5)
    end = time.perf_counter()
    print(test)
    print(f"Search time: {end - start:0.4f}")
