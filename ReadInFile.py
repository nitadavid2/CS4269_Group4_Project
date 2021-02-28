import openpyexcel as xl

# constants (enter file path names here)

FILE_PATH_WEIGHTS = "./input_files/Resources.xlsx"
FILE_PATH_INITSTATES = "./input_files/countries.xlsx"

# reads in the resource data
weightFrame = xl.load_workbook(FILE_PATH_WEIGHTS).active

resourcesDictionary = dict()
for row in weightFrame['A{}:F{}'.format(weightFrame.min_row + 1,weightFrame.max_row)]:
    resource = row[0].value
    data_list = list()

    data = row[1:len(row)]

    for cell in data:
        data_list.append(cell.value)

    # print(data_list)
    resourcesDictionary[resource] = data_list

# print(resourcesDictionary)

# reads in the initial country states
initStates = xl.load_workbook(FILE_PATH_INITSTATES).active

countryDictionary = dict()
for row in initStates['A{}:F{}'.format(initStates.min_row + 1,initStates.max_row)]:
    country = row[0].value
    data_list = list()

    data = row[1:len(row)]

    for cell in data:
        data_list.append(cell.value)

    # print(data_list)
    countryDictionary[country] = data_list

# print(countryDictionary)


# uses a dot product to produces a weighted resource sum (One possible
# metric of state quality) for each nation.
# Do we still need this?
# initStates["Weighted Resource Sum"] = initStates.loc[:, "R1":"R23'"].dot(weightFrame.loc[:, "Resource":"Weight"])
