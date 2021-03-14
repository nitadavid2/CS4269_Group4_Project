import ReadInFile
from Classes import State
import queue
import time


# a_star_search:
# Implement a search algorithm based on A* algorithm. The specific implementation we use
# does not currently use a heuristic (so it is more like a greedy search algorithm for now).
# In addition, this is a depth limited algorithm, so the most promising successors that
# do not violate the depth limit are explored before less promising successors. The function is designed
# to either run to completion or it can be modified with a timer/frontier limit to behave like
# an "anytime algorithm."
def a_star_search(start, depth):
    # We will use a priority queue for the A* implementation.
    # We will expand the frontier each time by expanding the "best path" using the
    # -(expected utility - utility) as priority.
    search_queue = queue.PriorityQueue()

    # We will have a queue of possible, valid paths discovered in the search
    solution_queue = queue.PriorityQueue()

    # A "schedule" is defined as list of actions (transfers or transforms)

    # Initialize search_queue
    for suc in start.findSuccessor():
        # Use -util since PriorityQueue.get() takes item with lowest priority
        # if eu >= 10:
        search_queue.put((-suc.eu, suc))

    # Explore search_queue
    while search_queue.qsize() > 0:
        next_item = search_queue.get()
        next_state_value, next_state = next_item[0], next_item[1]

        # Push current state to queue storing possible solutions
        solution_queue.put(next_item)

        # Before we go on, check current depth
        if next_state.depth < depth:
            # Now generate successors
            for suc in next_state.findSuccessor():
                # Add to queue
                # if eu >= 10:
                search_queue.put((-suc.eu, suc))

    answer_path = []
    # Return best option
    for i in range(5):
        if solution_queue.empty():
            break
        answer_item = solution_queue.get()
        answer_value = -answer_item[0]
        answer_path = answer_item[1].path

        # Print statements that report best solution found
        print("Number of solutions: ", solution_queue.qsize())
        print("Best solution EU: ", answer_value)
        print("Best Path: ", answer_path)

    return answer_path


if __name__ == '__main__':
    country_dict = ReadInFile.getCountryDict()
    start_state = State(0, country_dict, [])
    start = time.perf_counter()
    test = a_star_search(start_state, 2)
    end = time.perf_counter()
    print(f"Search time: {end - start:0.4f}")
