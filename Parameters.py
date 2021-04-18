# Parameters to use in Country Simulation Project

# Global Parameters
num_rounds = 5
frontier_size = 100

use_dynamic_limits = True  # Calculate solution_limit and depth limit dynamically based on country properties ?
solution_limit = 1000
depth = 3

seed = 123456654321


# Game Input Files
initial_state_filename = "./input_files/countries_for_test.xlsx"


# Game Output Files
output_schedule_filename = "./output_files/equal2.txt"  # Output - Print for each search best EU and path.

game_state_print = True  # Print game state ?
game_state_filename = "./game_output_files/Output5.csv"  # Game State Delta State Quality outputs
