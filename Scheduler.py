import ReadCountries
import ReadInterventions
import InterventionManager
import random
from Classes import State
import queue
import time

seed = 123456654321


def a_star_search(start, depth, f, solution_limit, player, type):
    """
    Implement a search algorithm based on A* algorithm. The specific implementation we use
    does not currently use a heuristic (so it is more like a greedy search algorithm for now).
    In addition, this is a depth limited algorithm, so the most promising successors that
    do not violate the depth limit are explored before less promising successors. The function is designed
    to either run to completion or it can be modified with a timer/frontier limit to behave like
    an "anytime algorithm."
    :param start: the start state.
    :param depth: the depth limit
    :return: The best solution (expected utility) found.
    """
    # We will use a priority queue for the A* implementation.
    # We will expand the frontier each time by expanding the "best path" using the
    # -(expected utility - utility) as priority.
    search_queue = queue.PriorityQueue()

    # We will have a queue of possible, valid paths discovered in the search
    solution_queue = queue.PriorityQueue()

    # A "schedule" is defined as list of actions (transfers or transforms)

    # Keeps track of solutions explored
    count = 0

    # Open output file

    # Initialize search_queue
    for suc in start.findSuccessor(player, type):
        # Use -util since PriorityQueue.get() takes item with lowest priority
        # if eu >= 10:
        search_queue.put((-suc.eu, suc))

    def print_solution(answer_item):
        answer_value = -answer_item[0]
        answer_path = answer_item[1].path

        # TODO: Remove after testing.
        f.write("Number of solutions: %d\n" % (solution_queue.qsize() + 1))
        f.write("Best solution EU: %d\n" % answer_value)
        f.write("Best Path: \n")
        for action in answer_path:
            f.write("%s\n" % (action, ))

    # Explore search_queue
    while search_queue.qsize() > 0:
        next_item = search_queue.get()
        next_state_value, next_state = next_item[0], next_item[1]

        # Push current state to queue storing possible solutions
        solution_queue.put(next_item)
        count = count + 1
        #if count == 1 or count == 5 or count == 10 or count == 50 or count == 100 or count == 500 or count == 1000:
        #    answer_item = solution_queue.get()
        #    print_solution(answer_item)
        #    solution_queue.put(answer_item)
        if count == solution_limit:
            break

        # Before we go on, check current depth
        if next_state.depth < depth:
            # Now generate successors
            for suc in next_state.findSuccessor(player, type):
                # Add to queue
                search_queue.put((-suc.eu, suc))

    # Return best option
    answer_item = solution_queue.get()
    print_solution(answer_item)
    other = "testing"
    if type == "transfer":
        other = answer_item[1].path[0][1]
    answer_item[1].path = []
    answer_item[1].depth = 0
    return answer_item[1], other

initial_state_filename = "./input_files/countries.xlsx"
output_schedule_filename = "./output_files/equal2.txt"
num_rounds = 3
solution_limit = 100
if __name__ == '__main__':
    country_dict = ReadCountries.getCountryDict(initial_state_filename)
    cur_state = State(0, country_dict, [])

    # Set random "seed"
    random.seed(seed)

    # interventions
    ints = ReadInterventions.getInterventions()
    print("Possible Interventions: ", ints)

    start = time.perf_counter()
    f = open(output_schedule_filename, "w")
    for i in range(num_rounds):
        for key in country_dict:
            cur_state = InterventionManager.intervention_manager(cur_state, key)
            solution_limit = (country_dict[key].resources["population"] - 9000) / 100
            depth = (country_dict[key].resources["population"] - 8000) / 1000
            cur_state, notpartner = a_star_search(cur_state, depth, f, solution_limit, key, "transform")
            proposed_state, partner = a_star_search(cur_state, 1, f, solution_limit, key, "transfer")
            accept, notpartner = a_star_search(proposed_state, depth, f, solution_limit, partner, "transform")
            decline, notpartner = a_star_search(cur_state, depth, f, solution_limit, partner, "transform")
            if accept.eu >= decline.eu:
                cur_state = proposed_state
                print("accepted transfer")
            else:
                print("declined transfer")

    #    cur_state, notpartner = a_star_search(cur_state, 4, f, solution_limit, key, "transform")
    end = time.perf_counter()
    f.close()
    print(f"Execution time: {end - start:0.4f}")
