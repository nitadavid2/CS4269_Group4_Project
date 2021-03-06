import ResourceQuality
import BasicOperations


class Country:
    def __init__(self, countryName, resources, resource_dict, init_state_quality):
        self.name = countryName
        self.resources = resources
        self.resource_dict = resource_dict
        self.init_state_quality = init_state_quality
        self.undiscounted_reward = 0
        self.discounted_reward = 0
        self.participation_prob = -1

    def state_quality(self):
        return ResourceQuality.getStateQuality(self.resources, self.resource_dict)

    def calc_rawutility(self):
        return 0


class State:
    def __init__(self, depth, countries, schedule):
        self.countries = countries
        self.depth = depth
        self.path = schedule

    def findSuccessor(self):
        def successors_for_transform(path, countries, depth):
            for quantity in quantity_choices:
                for transform_type in transform_types:
                    a, b = BasicOperations.transform(country, resources, quantity, transform_type)
                    if a:
                        path_to_update = path.copy()
                        countries_to_update = countries.copy()
                        path_to_update.append(a)
                        countries_to_update[country] = b
                        new_state = State(depth + 1, countries_to_update, path_to_update)
                        successor_list.append(new_state)

        def successors_for_transfer(path, countries, depth):
            successor_list.append([])

        quantity_choices = [2 ** 0, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5, 2 ** 6]
        transform_types = ['housing', 'food', 'electronics', 'metalAlloys']
        transfer_resource_type = ['metalElements', 'timber', 'metalAlloys', 'electronics', 'food',
                                  'metalAlloysWaste', 'housingWaste', 'electronicsWaste', 'foodWaste']
        successor_list = list()
        country = 'MyCountry'
        resources = self.countries[country].resources
        successors_for_transform(self.path, self.countries, self.depth)
        successors_for_transfer(self.path, self.countries, self.depth)

        return successor_list

    def undiscounted_reward(self, country):
        return country.state_quality() - country.init_state_quality

    def discounted_reward(self, gamma, country):
        return gamma ** self.depth * self.undiscounted_reward(country)

