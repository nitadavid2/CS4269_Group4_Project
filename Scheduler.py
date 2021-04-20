import Parameters as param
import ReadCountries
import ReadInterventions
import InterventionManager
import BasicOperations
import ResourceQuality
import random
from Classes import State
from depq import DEPQ
import queue
import time


seed = param.seed


def print_solution(answer_item, count):
    answer_value = -answer_item[1]
    answer_path = answer_item[0].path

    # Print state after each search.
    f.write("Number of solutions: %d\n" % (count + 1))
    f.write("Best solution EU: %d\n" % answer_value)
    f.write("Best Path: \n")
    for action in answer_path:
        f.write("%s\n" % (action, ))
    f.write("******************\n\n")


# Inspired by group 5
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
        adjusted_next_item = next_item[0], -next_item[1]

        next_state_value, next_state = next_item[1], next_item[0]
        solution_queue.put(adjusted_next_item)

        count = count + 1
        if next_state.depth < depth:
            for suc in next_state.findSuccessor(player, type):
                search_queue.insert(suc, suc.eu)
    other = "No trade"
    if solution_queue.empty():
        answer_item = (start, start.eu)
    else:
        answer_item = solution_queue.get(False)
        if (type == "transfer" or type == "war"):
            other = answer_item[0].path[0][1]
    print_solution(answer_item, solution_queue.qsize())

    answer_item[0].path = []
    answer_item[0].depth = 0
    return answer_item[0], other


initial_state_filename = param.initial_state_filename
output_schedule_filename = param.output_schedule_filename
game_state_print = param.game_state_print
game_state_filename = param.game_state_filename

num_rounds = param.num_rounds
frontier_size = param.frontier_size
use_dynamic_solution_limit = param.use_dynamic_solution_limit
use_dynamic_depth_limit = param.use_dynamic_depth_limit
solution_limit = param.solution_limit
depth = param.depth

interventions_on = param.interventions_on


if __name__ == '__main__':
    country_dict = ReadCountries.getCountryDict(initial_state_filename)
    cur_state = State(0, country_dict, [])

    # Set random "seed"
    random.seed(seed)

    # interventions
    ints = ReadInterventions.getInterventions()
    print("Possible Interventions: ", ints)

    # Start state

    start = time.perf_counter()
    f = open(output_schedule_filename, "w")
    for i in range(num_rounds):
        for key in country_dict:

            if interventions_on:
                cur_state = InterventionManager.intervention_manager(cur_state, key)

            if use_dynamic_solution_limit:
                solution_limit = (country_dict[key].resources["population"] - 9000) / 100
            if use_dynamic_depth_limit:
                depth = (country_dict[key].resources["population"] - 8000) / 1000
            cur_state, notpartner = search(cur_state, depth, f, solution_limit, key, "transform", frontier_size)
            proposed_state, partner = search(cur_state, 1, f, solution_limit, key, "transfer", frontier_size)
            if partner != "No trade":
                accept, notpartner = search(proposed_state, depth, f, solution_limit, partner, "transform", frontier_size)
                decline, notpartner = search(cur_state, depth, f, solution_limit, partner, "transform", frontier_size)
                if accept.eu >= decline.eu:
                    cur_state = proposed_state
                    print("accepted transfer")
                else:
                    print("declined transfer")
            else:
                cur_state = proposed_state
            war_goal, target = search(cur_state, 1, f, solution_limit, key, "war", frontier_size)
            if target != "No trade":
                cur_state = BasicOperations.war(key, target, cur_state, True, seed)
                print("War occurs")

            # Iterate through country - set init_state to current
            for c_name in cur_state.countries:
                country = cur_state.countries[c_name]
                country.init_state_quality = ResourceQuality.getStateQuality(country.resources)

    #    cur_state, notpartner = a_star_search(cur_state, 4, f, solution_limit, key, "transform")
    end = time.perf_counter()
    f.close()

    if game_state_print:
        cur_state.current_output(game_state_filename)

    print(f"Execution time: {end - start:0.4f}")
