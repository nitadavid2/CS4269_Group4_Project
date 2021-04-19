import ReadCountries
from Classes import State
import queue
import time
import Inequality


def a_star_search(start, depth, output_schedule_filename, solution_limit):
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
    f = open(output_schedule_filename, "w")

    # Initialize search_queue
    for suc in start.findSuccessor():
        # Use -util since PriorityQueue.get() takes item with lowest priority
        # if eu >= 10:
        search_queue.put((-suc.eu, suc))

    def print_solution(answer_item):
        answer_value = -answer_item[0]
        answer_state = answer_item[1]
        answer_path = answer_state.path

        # TODO: Remove after testing.
        f.write("Number of solutions: %d\n" % (solution_queue.qsize() + 1))
        f.write("Best solution EU: %d\n" % answer_value)
        f.write("MLD: %f\n" % Inequality.mean_log_dev(answer_state))
        f.write("ARQ: %f\n" % Inequality.actor_rel_quality(answer_state))
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
        if count == 1 or count == 5 or count == 10 or count == 50 or count == 100 or count == 500 or count == 1000:
            answer_item = solution_queue.get()
            print_solution(answer_item)
            solution_queue.put(answer_item)
        if count == solution_limit:
            break

        # Before we go on, check current depth
        if next_state.depth < depth:
            # Now generate successors
            for suc in next_state.findSuccessor():
                # Add to queue
                search_queue.put((-suc.eu, suc))

    # Return best option
    answer_item = solution_queue.get()
    print_solution(answer_item)

    f.close()
    return answer_item[1]

initial_state_filename = "./input_files/MLD0.5_ARQ2.xlsx"
initial_resources_filename = "./input_files/Resources.xlsx"
output_schedule_filename = "./output_files/MD0.5_ARQ2.txt"
depth = 2
solution_limit = 100
if __name__ == '__main__':
    country_dict = ReadCountries.getCountryDict(initial_state_filename)
    start_state = State(0, country_dict, [])
    start = time.perf_counter()
    print("IN_MLD: ", Inequality.mean_log_dev(start_state))
    print("IN_ARQ: ", Inequality.actor_rel_quality(start_state))
    test = a_star_search(start_state, depth, output_schedule_filename, solution_limit)
    print("\nOUT_MLD: ", Inequality.mean_log_dev(test))  # MLD
    print("OUT_ARQ: ", Inequality.actor_rel_quality(test))  # Rel. Quality
    end = time.perf_counter()
    print(f"Search time: {end - start:0.4f}")
