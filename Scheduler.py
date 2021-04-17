import ReadCountries
import ReadInterventions
import InterventionManager
import random
from Classes import State
from depq import DEPQ
import queue
import time

seed = 123456654321

def print_solution(answer_item, count):
    answer_value = -answer_item[1]
    answer_path = answer_item[0].path

    # TODO: Remove after testing.
    f.write("Number of solutions: %d\n" % (count + 1))
    f.write("Best solution EU: %d\n" % answer_value)
    f.write("Best Path: \n")
    for action in answer_path:
        f.write("%s\n" % (action, ))

# inpsired by group 5
def search(start, depth, file, solution_limit, player, type, frontier_size):
    search_queue = DEPQ(maxlen=frontier_size)
    for suc in start.findSuccessor(player, type):
        # Use -util since PriorityQueue.get() takes item with lowest priority
        # if eu >= 10:
        search_queue.insert(suc, suc.eu)

    solution_queue = queue.PriorityQueue()

    count = 0
    while not search_queue.is_empty() and count < solution_limit:
        next_item = search_queue.popfirst()
        next_state_value, next_state = next_item[1], next_item[0]
        solution_queue.put(next_item)
        count = count + 1
        if next_state.depth < depth:
            for suc in next_state.findSuccessor(player, type):
                search_queue.insert(suc, suc.eu)
    answer_item = solution_queue.get()
    print_solution(answer_item, solution_queue.qsize())
    other = "testing"
    if type == "transfer":
        other = answer_item[0].path[0][1]
    answer_item[0].path = []
    answer_item[0].depth = 0
    return answer_item[0], other


initial_state_filename = "./input_files/countries.xlsx"
output_schedule_filename = "./output_files/equal2.txt"
num_rounds = 2
#solution_limit = 10000
#depth = 10
frontier_size = 100

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
            cur_state, notpartner = search(cur_state, depth, f, solution_limit, key, "transform", frontier_size)
            proposed_state, partner = search(cur_state, 1, f, solution_limit, key, "transfer", frontier_size)
            accept, notpartner = search(proposed_state, depth, f, solution_limit, partner, "transform", frontier_size)
            decline, notpartner = search(cur_state, depth, f, solution_limit, partner, "transform", frontier_size)
            if accept.eu >= decline.eu:
                cur_state = proposed_state
                print("accepted transfer")
            else:
                print("declined transfer")
            

    #    cur_state, notpartner = a_star_search(cur_state, 4, f, solution_limit, key, "transform")
    end = time.perf_counter()
    f.close()
    print(f"Execution time: {end - start:0.4f}")
