import ResourceQuality
import BasicOperations
import copy
import math
import csv


class Country:
    """
    A class that defines the country object for every country in our countries dictionary. Each country object contains
    all kinds of information for this country.
    """
    def __init__(self, countryName, resources, init_state_quality):
        """
        Initializing the country's name, resources, initial state quality, and participation probability here.
        :param countryName: String for the country's name
        :param resources: A dictionary containing the amounts of resources in the country
        :param init_state_quality: Int for the initial state quality of the country
        """
        self.name = countryName
        self.resources = resources
        self.init_state_quality = init_state_quality
        self.participation_prob = -1


class State:
    """
    A class that defines the country object for every state in our search tree. Each state object contains information
    of all countries' resources states and the path to get to the state from the starting state in the search tree.
    """
    def __init__(self, depth, countries, schedule):
        """
        Initializing the stat
        e's countries dictionary, depth, path, and expected utility here.
        :param depth: Int for the depth of the state in the search tree
        :param countries: A dictionary containing country objects
        :param schedule: A list for the initial schedule
        """
        self.countries = countries
        self.depth = depth
        self.path = schedule
        self.eu = 0

    # Define the notion of '<' for a State, used in PriorityQueue when priority of
    # two states is otherwise equal. We prefer the lower depth in that case
    def __lt__(self, other):
        return self.depth < other.depth

    def findSuccessor(self, player, type):
        """
        This function finds all possible successor states for the given state. It contains two inner functions:
        successors_for_transform and successors_for_transfer which find successor states for different TRANSFORM and
        TRANSFER operations respectively.
        :return: A tuple containing all the states found.
        """

        def successors_for_transform(path, countries, depth, player):
            """
            This function finds all possible successor states after performing TRANSFORM for the given state. I explores
            all possible TRANSFORM operations for MyCountry in this state and only passes in states whose expected
            utilities are higher than the threshold.
            :param path: A list indicating the given state's path
            :param countries: A dictionary indicating all of the countries in the given state's
            :param depth: Int indicating the given state's schedule depth in the search tree
            """
            # go through the list of different quantities for TRANSFORM operator which determine the resource
            # amount that MyCountry can get in this TRANSFORM
            for quantity in quantity_choices:

                # go through different types of resources that MyCountry can get in this TRANSFORM
                for transform_type in transform_types:

                    # perform the TRANSFORM operator
                    a, b = BasicOperations.transform(player, resources, quantity, transform_type)

                    # look at the new state if the operator is successfully performed
                    if a:

                        # get initial state quality of MyCountry in order to calculate the probability that the country
                        # participates in the schedule
                        init_state = countries[player].init_state_quality

                        # calculate the probability: d_r as the discounted reward and par_p as the probability
                        d_r, par_p = self.country_participation_probability(b, init_state, 0.9, depth + 1, 0, 1)

                        # First calculate the schedule success probability by multiplying the participation probability
                        # of all countries involved in the schedule. Then calculate the expected utility of this
                        # schedule.
                        p = 1
                        for i in countries:

                            # multiply all involved countries' participation probability except MyCountry
                            if i != player and countries[i].participation_prob != -1:
                                p = p * countries[i].participation_prob

                        # get utility by multiply p with MyCountry's participation probability and discounted reward
                        eu = p * par_p * d_r

                        # only generate and append the state to the list if the expected utility is larger than the
                        # threshold
                        if eu >= 100000:
                            path_to_update = copy.deepcopy(path)
                            countries_to_update = copy.deepcopy(countries)

                            # update the path (schedule)
                            a += ("EU: %d" % eu, )
                            path_to_update.append(a)

                            # update MyCountry's resources dictionary
                            countries_to_update[player].resources = b

                            # update MyCountry's participation probability
                            countries_to_update[player].participation_prob = par_p

                            # create new state
                            new_state = State(depth + 1, countries_to_update, path_to_update)

                            # update expected utility of the new state
                            new_state.eu = eu

                            # append new state to the successor state list
                            successor_list.append(new_state)

        def successors_for_transfer(path, countries, depth, player):
            """
            This function finds all possible successor states after performing TRANSFER for the given state. I explores
            all possible TRANSFER operations for MyCountry in this state and only passes in states whose expected
            utilities are higher than the threshold.
            :param path: A list indicating the given state's path
            :param countries: A dictionary indicating all of the countries in the given state's
            :param depth: Int indicating the given state's schedule depth in the search tree
            """
            # go through the list of different quantities for TRANSFER operator which determine the resource
            # amount that MyCountry can get in this TRANSFER
            for quantity in quantity_choices_1:

                # create a unit price list without the wastes
                positive_resource_unit_prices = transfer_unit_prices[0:6]

                # go through the list of different desired resources in this TRANSFER operation
                for desired_resource in positive_resource_unit_prices:

                    # create a resource list for step 2 of the trade (give out resources or accept wastes) by removing
                    # the chosen desired resource in the resource list in order to explore different trading
                    # possibilities (we only trade for desired resources by giving other resources or accepting wastes)
                    other_resources = transfer_unit_prices.copy()
                    other_resources.remove(desired_resource)

                    # go though the dictionary of countries as potential target countries in this TRANSFER trade
                    for target_c in countries:

                        # only trade with other countries
                        if target_c != player:

                            # go through the list of resources without the desired resource to perform different
                            # possible trades
                            for r in other_resources:

                                # perform step 1 of the trade by doing one TRANSFER (MyCountry accepts desired
                                # resources from the target country)
                                a1, b1, c1 = BasicOperations.transfer(target_c, player,
                                                                      countries[target_c].resources, resources,
                                                                      desired_resource[0], quantity)

                                # calculate the amount of resource we give out or the amount of waste we accept in the
                                # second phase of the trade
                                trade_amount = desired_resource[1] * quantity / abs(r[1])

                                # perform step 2 of the trade (when we choose to accept wastes)
                                if 'Waste' in r[0]:
                                    a2, b2, c2 = BasicOperations.transfer(target_c, player, b1,
                                                                          c1, r[0], trade_amount)
                                # perform step 2 of the trade (when we choose to give out other resources)
                                else:
                                    a2, c2, b2 = BasicOperations.transfer(player, target_c, c1,
                                                                          b1, r[0], trade_amount)

                                # look at the new state if the 2 TRANSFER operators for both steps of the trade are
                                # successfully performed
                                if a1 and a2:

                                    # get initial state quality of MyCountry and the other country in the trade in
                                    # order to calculate the probability that the countries participate in the schedule
                                    init_state1 = countries[target_c].init_state_quality
                                    init_state2 = countries[player].init_state_quality

                                    # calculate the probabilities for both countries: d_r as the discounted reward and
                                    # par_p as the probability
                                    d_r1, par_p1 = self.country_participation_probability(b2, init_state1, 0.9,
                                                                                          depth + 1, 0, 1)
                                    d_r2, par_p2 = self.country_participation_probability(c2, init_state2, 0.9,
                                                                                          depth + 1, 0, 1)

                                    # First calculate the schedule success probability by multiplying the participation
                                    # probability of all countries involved in the schedule. Then calculate the expected
                                    # utility of this schedule.
                                    p = 1
                                    for i in countries:

                                        # multiply all involved countries' participation probability except the two
                                        # countries involved in the trade
                                        if i != target_c and i != player and countries[i].participation_prob != -1:
                                            p = p * countries[i].participation_prob

                                    # get utility by multiply p with both countries' participation probabilities and
                                    # MyCountry's discounted reward
                                    eu = p * par_p1 * par_p2 * d_r2

                                    # only generate append the state to the list if the expected utility is larger than
                                    # the threshold
                                    if eu >= 100000:
                                        path_to_update = copy.deepcopy(path)
                                        countries_to_update = copy.deepcopy(countries)

                                        # update the path (schedule)
                                        a1 += ("EU: %d" % eu, )
                                        a2 += ("EU: %d" % eu, )
                                        path_to_update.append(a1)
                                        path_to_update.append(a2)

                                        # update both countries' resources dictionaries
                                        countries_to_update[target_c].resources = b2
                                        countries_to_update[player].resources = c2

                                        # update both countries' participation probabilities
                                        countries_to_update[target_c].participation_prob = par_p1
                                        countries_to_update[player].participation_prob = par_p2

                                        # generate new state
                                        new_state = State(depth + 1, countries_to_update, path_to_update)

                                        # update the expected utility in the new state
                                        new_state.eu = eu

                                        # append the new state to the successor state list
                                        successor_list.append(new_state)

        # define quantity choices list for TRANSFORM successor function
        quantity_choices = (2 ** 0, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 5, 2 ** 6)

        # define quantity choices list for TRANSFER successor function
        quantity_choices_1 = (1, 10, 100)

        # define TRANSFORM type list for TRANSFORM successor function
        transform_types = ('housing', 'food', 'electronics', 'metalAlloys')

        # define unit prices list for TRANSFER successor function
        transfer_unit_prices = [('metalElements', 2100), ('timber', 200), ('metalAlloys', 2200),
                                ('electronics', 4300), ('food', 180), ('water', 2),
                                ('metalAlloysWaste', -53), ('housingWaste', -53),
                                ('electronicsWaste', -53), ('foodWaste', -53)]

        # initialize the successor state list
        successor_list = list()

        # MyCountry's resources dictionary
        resources = self.countries[player].resources

        # finding all possible successor states from both TRANSFORM and TRANSFER
        if type == "transform":
            successors_for_transform(self.path, self.countries, self.depth, player)
        if type == "transfer":
            successors_for_transfer(self.path, self.countries, self.depth, player)

        return tuple(successor_list)

    def country_participation_probability(self, resources, init_s, gamma, depth, x_0, k, L=1):
        """
        This function calculates the participation probability of a specific country.
        :param resources: A dictionary for the country's resources
        :param init_s: Int for the country's initial state
        :param gamma: Int for gamma in calculating discounted reward
        :param depth: Int for the successor state's depth
        :param x_0: Int for x_0 in calculating the country participation probability
        :param k: Int for k in calculating the country participation probability
        :param L: Int for L in calculating the country participation probability
        :return: An int for the discounted reward, an int for the country participation probability.
        """

        # finding the state quality for the country in the current state
        sq = ResourceQuality.getStateQuality(resources)

        # using delta state quality to calculate the discounted reward for the country
        dr = gamma ** depth * (sq - init_s)

        # calculate the country's participation probability
        cpp = L / (1 + math.exp(-k * (dr - x_0))) if -k * (dr - x_0) < 100 else -1

        return dr, cpp

    def current_output(self):
        csv_file = "./game_output_files/Output1.csv"
        csv_columns = ['Name', 'population', 'metalElements', 'timber', 'landArea', 'water', 'metalAlloys',
                       'electronics', 'housing', 'food', 'metalAlloysWaste', 'housingWaste', 'electronicsWaste',
                       'foodWaste', 'score']
        with open(csv_file, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            writer.writeheader()
            for i in self.countries:
                score = ResourceQuality.getStateQuality(self.countries[i].resources) - self.countries[i].init_state_quality
                s = {'score': score}
                a = {'Name': i}
                a.update(self.countries[i].resources)
                a.update(s)
                writer.writerow(a)
                print(a)
        csv_file.close()