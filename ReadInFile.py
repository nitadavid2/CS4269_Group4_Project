import pandas as pd

# constants (enter file path names here)

FILE_PATH_WEIGHTS = "./input_files/Resources.xlsx"
FILE_PATH_INITSTATES = "./input_files/countries.xlsx"


# reads in the country weights
weightFrame = pd.read_excel(FILE_PATH_WEIGHTS, "Resources")
print(weightFrame.head(4))

# reads in the initial country states
initStates = pd.read_excel(FILE_PATH_INITSTATES,"Countries")
print(initStates.head(3))

# uses a dot product to produces a weighted resource sum (One possible
# metric of state quality) for each nation.
initStates["Weighted Resource Sum"] = initStates.loc[:, "R1":"R23'"].dot(weightFrame.loc[:, "Resource":"Weight"])