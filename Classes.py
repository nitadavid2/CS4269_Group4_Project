import Parameters as param
import ResourceQuality
import BasicOperations as Ops
import copy
import math
import csv

res_dict = ResourceQuality.resourceDict

seed = param.seed


class Country:
    """
    A class that defines the country object for every country in our countries dictionary. Each country object contains
    all kinds of information for this country.
    """
    def __init__(self, countryName, resources, init_state_quality, prob_parameter, war_ambition):
        """
        Initializing the country's name, resources, initial state quality, and participation probability here.
        :param countryName: String for the country's name
        :param resources: A dictionary containing the amounts of resources in the country
        :param init_state_quality: Int for the initial state quality of the country
        :param prob_parameter: A list containing parameters for probability calculation in transfer successor function
        :param war_ambition: Long indicating the war ambition level of a country
        """
        self.name = countryName
        self.resources = resources
        self.init_state_quality = init_state_quality
        self.first_round_quality = init_state_quality
        self.participation_prob = -1
        self.war_quality = self.warfare_quality()
        self.prob_parameter = prob_parameter
        self.war_ambition = war_ambition

    def warfare_quality(self):
        """
        The warfare_quality function returns a number corresponding to the
        necessity of a country needing to resort to war to meet its needs.
        Return: a double corresponding to the necessity for the country to go to war.
        """
        war_Quality = 0
        for res in res_dict:

            set = res_dict[res]
            thresh1 = set[3]
            our_res = self.resources[res]
            warweight = set[8]

            #no the war weights yet
            war_Quality += (((thresh1 - our_res)/thresh1) * warweight)

        return war_Quality

    def deterrence_score(self, country):
        """
        The deterrence_score function returns a number corresponding to the fear
        a country has in taking on another specific country based on the relative weighting
        of the other's war power and the country's own war power.
        country: the name of the country to which self is being compared to.
        Return: a double representing the ratio of the potential opponent's power to the
        war power of self.
        """

        # Higher means other country is more powerful.
        det = (Ops.war_power(country)/Ops.war_power(self))

        return det

    def relationship_score(self, country):
        """
        The relationship_score function models the preference a country has to trading with
        another specific country as opposed to war with that other country.
        country: the name of the country to which self is being compared to.
        Return: a double representing the strength of the preference
        that self has to trading with the other country rather than
        resorting to war.
        """

        diff_dict = list()

        for res in res_dict:
            # Iterative look in dictionary
            data = res_dict[res]

            weight = data[0]  # Economic weights
            model = data[1]
            scaling = data[2]

            our_quantity = self.resources[res]
            country_quantity = country.resources[res]

            # Analyze diff (- of this is the advantage of other country to us)
            diff = our_quantity - country_quantity
            diff_dict.append(diff)

        # Now find max, min in diff_dict. Negate min and apply to formula. This
        # represents the amount of the difference between the countries most
        # unequal resource.
        MaxDiff_XY = max(diff_dict)
        MaxDiff_YX = -min(diff_dict)

        # Normalize by dividing max advantage over min advantage
        # This is 1 when countries have equal imbalances of resources, symbolizing high
        # potential for trade.
        min_Diff = min(MaxDiff_YX, MaxDiff_XY)
        max_Diff = max(MaxDiff_YX, MaxDiff_XY, 0.0000000001)

        return min_Diff/max_Diff

    def war_inclination(self, country):
        """
        The war_inclination function returns a single numeric value representing the potential
        gains vs. losses of self going to war with another specific country.
        country: the name of the country to which self is considering war with.
        Return: a double representing the inclination of self going to
        war with another specific country. The closer this is to 1, the more inclined
        the country is to war.
        """
        det = self.deterrence_score(country)
        rel = self.relationship_score(country)

        # This approaches 1 when countries really want war.
        # Countries can be really negative, but this doesn't matter to us.
        return 1 - det * rel


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
        :param player: A string indicating the player/country
        :param type: A string indicating the operation type
        :return: A tuple containing all the states found.
        """

        def successors_for_transform(path, countries, depth, player):
            """
            This function finds all possible successor states after performing TRANSFORM for the given state. It explores
            all possible TRANSFORM operations for the player in this state and only passes in states whose expected
            utilities are higher than the threshold.
            :param path: A list indicating the given state's path
            :param countries: A dictionary indicating all of the countries in the given state's
            :param depth: Int indicating the given state's schedule depth in the search tree
            :param player: String indicating the country/player
            """
            # go through the list of different quantities for TRANSFORM operator which determine the resource
            # amount that MyCountry can get in this TRANSFORM
            for quantity in quantity_choices:

                # go through different types of resources that MyCountry can get in this TRANSFORM
                for transform_type in transform_types:

                    # perform the TRANSFORM operator
                    a, b = Ops.transform(player, resources, quantity, transform_type)

                    # look at the new state if the operator is successfully performed
                    if a:

                        # get initial state quality of MyCountry in order to calculate the probability that the country
                        # participates in the schedule
                        init_state = countries[player].init_state_quality

                        # calculate the probability: d_r as the discounted reward and par_p as the probability
                        d_r, par_p = self.country_participation_probability(b, init_state, 0.9, depth + 1, 0, 1)

                        # get utility by multiply p with MyCountry's participation probability and discounted reward
                        eu = d_r

                        # only generate and append the state to the list if the expected utility is larger than the
                        # threshold
                        if eu > 0:
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
            This function finds all possible successor states after performing TRANSFER for the given state. It explores
            all possible TRANSFER operations for the player in this state and only passes in states whose expected
            utilities are higher than the threshold.
            :param path: A list indicating the given state's path
            :param countries: A dictionary indicating all of the countries in the given state's
            :param depth: Int indicating the given state's schedule depth in the search tree
            :param player: String indicating the country/player
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
                                a1, b1, c1 = Ops.transfer(target_c, player,
                                                                      countries[target_c].resources, resources,
                                                                      desired_resource[0], quantity)

                                # calculate the amount of resource we give out or the amount of waste we accept in the
                                # second phase of the trade
                                trade_amount = desired_resource[1] * quantity / abs(r[1])

                                # perform step 2 of the trade (when we choose to accept wastes)
                                if 'Waste' in r[0]:
                                    a2, b2, c2 = Ops.transfer(target_c, player, b1,
                                                                          c1, r[0], trade_amount)
                                # perform step 2 of the trade (when we choose to give out other resources)
                                else:
                                    a2, c2, b2 = Ops.transfer(player, target_c, c1,
                                                                          b1, r[0], trade_amount)

                                # look at the new state if the 2 TRANSFER operators for both steps of the trade are
                                # successfully performed
                                if a1 and a2:

                                    # get initial state quality of MyCountry and the other country in the trade in
                                    # order to calculate the probability that the countries participate in the schedule
                                    init_state1 = countries[target_c].init_state_quality
                                    init_state2 = countries[player].init_state_quality

                                    # prob_parameter1 as the k, x_0 for not trading selective countries, prob_parameter2
                                    # for selective countries
                                    prob_parameter1 = countries[target_c].prob_parameter
                                    prob_parameter2 = countries[player].prob_parameter

                                    # calculate the probabilities for both countries: d_r as the discounted reward and
                                    # par_p as the probability using the prob_parameter as an implementation of trading
                                    # strategies here
                                    d_r1, par_p1 = self.country_participation_probability(b2, init_state1, 0.9,
                                                                                          depth + 1, prob_parameter1[0],
                                                                                          prob_parameter1[1])
                                    d_r2, par_p2 = self.country_participation_probability(c2, init_state2, 0.9,
                                                                                          depth + 1, prob_parameter2[0],
                                                                                          prob_parameter2[1])

                                    # get utility by multiply p with both countries' participation probabilities and
                                    # MyCountry's discounted reward
                                    eu = par_p1 * d_r2

                                    # only generate append the state to the list if the expected utility is larger than
                                    # the threshold
                                    if eu > 0:
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

        def successors_for_war(path, countries, depth, player):
            """
            This function finds all possible successor states after performing WAR for the given state. It explores
            all possible WAR operations for the player in this state and only passes in states when warfare quality
            and war inclination function tell it that the war is appropriate.
            :param path: A list indicating the given state's path
            :param countries: A dictionary indicating all of the countries in the given state's
            :param depth: Int indicating the given state's schedule depth in the search tree
            :param player: String indicating the country/player
            """
            # check warfare quality here
            if countries[player].war_quality >= -1:

                for target_c in countries:
                    if target_c != player:
                        war_inclination = countries[player].war_inclination(countries[target_c])

                        # comparing war inclination and the country's war ambition to decide if go to war
                        if war_inclination >= countries[player].war_ambition:
                            path_to_update = copy.deepcopy(path)
                            countries_to_update = copy.deepcopy(countries)
                            init_state1 = countries[player].init_state_quality
                            new_state = State(depth + 1, countries_to_update, path_to_update)
                            new_state = Ops.war(player, target_c, new_state, False, seed)

                            # calculate participation probability for expected utility
                            d_r1, par_p1 = self.country_participation_probability(new_state.countries[player].resources, init_state1, 0.9,
                                                                                  depth + 1, 0, 1)

                            advantage = countries[player].war_quality - countries[target_c].war_quality\

                            eu = d_r1 * advantage
                            new_state.eu = eu

                            # check expected utility before appending the new state into the list
                            if eu > (1000 - (countries[player].war_ambition * 700)):
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
        if type == 'war':
            successors_for_war(self.path, self.countries, self.depth, player)

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
        if abs(dr) < 0.00001:
            cpp = L / (1 + math.exp(-k * (dr - x_0))) if -k * (dr - x_0) < 100 else -1
        else:
            if -(k ** ((dr - x_0) / abs((dr - x_0)) * -1)) * (dr - x_0) < 100:
                cpp = L / (1 + math.exp(-(k ** ((dr - x_0)/abs((dr - x_0)) * -1)) * (dr - x_0)))
            else:
                cpp = -1

        return dr, cpp

    def current_output(self, file_name):
        """
        current_output is a helper function that prints the current best path, and best path EU
        to a file.
        file_name: the path to write to.
        Return: void.
        """
        csv_file = file_name
        csv_columns = ['Name', 'population', 'metalElements', 'timber', 'landArea', 'water', 'metalAlloys',
                       'electronics', 'housing', 'food', 'metalAlloysWaste', 'housingWaste', 'electronicsWaste',
                       'foodWaste', 'score']
        with open(csv_file, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            writer.writeheader()
            for i in self.countries:
                score = ResourceQuality.getStateQuality(self.countries[i].resources) - self.countries[i].first_round_quality
                s = {'score': score}
                a = {'Name': i}
                a.update(self.countries[i].resources)
                a.update(s)
                writer.writerow(a)
        csv_file.close()
