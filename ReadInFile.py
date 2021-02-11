import pandas as pd

# constants (enter file path names here)
FILE_PATH_WEIGHTS = "./input_files/country_weights.csv"
FILE_PATH_INITSTATES = "./input_files/initial_states.csv"


# reads in the country weights
weightFrame = pd.read_csv(FILE_PATH_WEIGHTS).set_index("Resource")

# reads in the initial country states
initStates = pd.read_csv(FILE_PATH_INITSTATES)


# uses a dot product to produces a weighted resource sum (One possible
# metric of state quality) for each nation.
initStates["Weighted Resource Sum"] = initStates.loc[:, "R1":"R23'"].dot(weightFrame["Weight"])