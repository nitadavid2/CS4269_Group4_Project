import ReadInFile as data


class Country:
    def __init__(self, countryName):
        self.resources = dict
        self.name = countryName

    def stateQuality(self):
        return 0

    def readCountryResource(self):
        ptr = data.initStates

        self.resources
        return 0

    def getPopulation(self):
        return self.resources.get("population");


class State:
    def __init__(self, countries, schedule = [], depth = 0):
        self.countries = countries
        self.depth = depth
        self.path = schedule

    def findSuccessor(self, actions):
        return 0

    def discountedReward(self,country):
        return 0
