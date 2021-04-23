import openpyxl as xl
from ResourceQuality import getStateQuality
from Classes import Country
import Parameters


def getCountryDict(FILE_PATH_INITSTATES):
    """
    Read countries information from countries.xlsx file, create country object for every country in the list, and pass
    in all the information to a dictionary.
    :return A dictionary containing all country objects
    """
    # reads in the initial country states
    initStates = xl.load_workbook(FILE_PATH_INITSTATES, data_only=True).active

    countryDictionary = dict()
    resource_list = [i.value for i in initStates[1] if i.value != 'Country']

    for row in initStates['A{}:P{}'.format(initStates.min_row + 1, initStates.max_row)]:
        country = row[0].value
        data_dict = {}

        data = row[1:len(row)-2]
        trade_selectivity = row[len(row)-2].value
        war_ambition = row[len(row)-1].value

        for i in range(len(data)):
            data_dict[resource_list[i]] = data[i].value

        # print(data_list)
        init_state_quality = getStateQuality(data_dict)
        selectivity_parameter = Parameters.trade_selectivity_parameters
        if trade_selectivity == 0:
            prob_parameter = [selectivity_parameter[0], selectivity_parameter[1]]
        else:
            prob_parameter = [selectivity_parameter[2], selectivity_parameter[3]]
        countryDictionary[country] = Country(country, data_dict, init_state_quality, prob_parameter, war_ambition)

    return countryDictionary
