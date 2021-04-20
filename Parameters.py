# Parameters to use in Country Simulation Project

# Global Parameters
num_rounds = 5
frontier_size = 100

  # Calculate solution_limit and depth limit dynamically based on country properties ?
use_dynamic_solution_limit = True
use_dynamic_depth_limit = True
solution_limit = 1000
depth = 3

interventions_on = True  # Do we want interventions ?

seed = 123456654321


# Game Input Files
initial_state_filename = "./input_files/countries_for_test.xlsx"
initial_resource_filename = "./input_files/Resources.xlsx"
initial_interventions_filename = "./input_files/Interventions_case0.xlsx"


# Game Output Files
output_schedule_filename = "./output_files/equal2.txt"  # Output - Print for each search best EU and path.

game_state_print = True  # Print game state ?
game_state_filename = "./game_output_files/Output5.csv"  # Game State Delta State Quality outputs
