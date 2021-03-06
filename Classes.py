import pandas as pd
import ResourceQuality


class Country:
    def __init__(self, countryName, resources, resource_dict, init_state_quality):
        self.name = countryName
        self.resources = resources
        self.resource_dict = resource_dict
        self.init_state_quality = init_state_quality
        self.undiscounted_reward = 0
        self.discounted_reward = 0

    def state_quality(self):
        return ResourceQuality.getStateQuality(self.resources, self.resource_dict)

    def calc_rawutility(self):
        return 0


class State:
    def __init__(self, depth, countries, schedule):
        self.countries = countries
        self.depth = depth
        self.path = schedule

    def findSuccessor(self, actions):
        #TODO: Implement successor generator function
        return 0

    def undiscounted_reward(self, country):
        return country.state_quality() - country.init_state_quality

    def discounted_reward(self, gamma, country):
        return gamma ** self.depth * self.undiscounted_reward(country)

