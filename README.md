# CS4269 Group4 Project

README:
### Setup For A simulation
We simulate the gradual, turn-based evolution of a world of N virtual countries, each with M resources and some amount of each resource, including possibly zero units of some resources.

Files needed: 
BasicOperations.py, Classes.py, Parameters.py, ReadCountries.py,  ReadResources.py, Resources.py, ResourceQuality.py, Scheduler.py

Execution instructions :

* Required dependencies:

        - DEPQ: “pip install depq”

        - openpyxl: “pip install openpyxl”

        - Numpy: “pip install numpy”

* Clone or download a zip file for the project
* open terminal and cd into the project directory
* Define execution parameters in Parameters.py
* Run python Scheduler.py to execute the simulation

### Overview of Simulation
Our program is built from several different subcomponent portions. The major components include a file containing global variables and parameters in Parmeters.py, definitions of Country and State Classes, the definition of key helper functions in BasicOperations.py, the search and main function in Scheduler.py, and several helper files that implement functions to read in the input files and manage game operations based on the input files.

A diagram of the system architecture is included below. The arrows from the Parameters.py file to the other files indicate that the Parameters.py file defines key global variables throughout the simulation code. The arrow between State and Country shows that a Country is contained within a State.

### Data structure or code structure

![Diagram here](/diagram.png)

The main top-level functions are the main function in Scheduler.py. This function takes no parameters from the console. The parameters are instead defined in the Parameters.py file, the main function understands where to find the needed input files based on the defined parameters in the Parameters.py file. The search function, the transfer, transform, and war operators, the find_successor function, and the country_participation_probability function are the other high-level functions.

#### Main function:


#### Search function:


#### Transform operator:
This function passes parameters to different TRANSFORM functions based on the value of transform_type.

:param country: String of country's name

:param resources: A dictionary containing the amounts of resources in the country

:param n: Number multiplied to increase the transformation yield

:param transform_type: String indicating the type of transform

:return: Operator summary and updated resources dictionary.

#### Transfer operator:
This TRANSFER function makes changes to both the sender and the receiver's dictionaries based on the resource
type and the trading amount for the TRANSFER.

:param sender: String of sender country's name

:param receiver: String of receiver country's name

:param sender_resources: A dictionary containing the amounts of resources in the sender country

:param receiver_resources: A dictionary containing the amounts of resources in the receiver country

:param transfer_resource: String of the resource type for this TRANSFER

:param amount: Int of the trading amount for this TRANSFER

:return: Operator summary and updated resources dictionary.

#### War operator:
The war function models the occurrence of a war between nations, including the outcome if desired.
The function returns the state of the game world after the war is simulated, if desired, or otherwise
the state where attacker always wins.

attacker: the name of the attacking country.

defender: the name of the defending country.

state: the world state at the time of war commencement.

determine: should the outcome of the war be simulated? False by default, which returns the state assuming the attacker always wins.

seed: the random number generator seed, None by default.

Return: the state after war has been simulated, if desired, or after attacker is assumed to win.

#### find_successor :
This function finds all possible successor states for the given state. It contains two inner functions:
successors_for_transform and successors_for_transfer which find successor states for different TRANSFORM and TRANSFER operations respectively.

:param player: A string indicating the player/country

:param type: A string indicating the operation type

:return: A tuple containing all the states found.

#### Country_participation_probability: 
        This function calculates the participation probability of a specific country.
        
        :param resources: A dictionary for the country's resources
        
        :param init_s: Int for the country's initial state
        
        :param gamma: Int for gamma in calculating discounted reward
        
        :param depth: Int for the successor state's depth
        
        :param x_0: Int for x_0 in calculating the country participation probability
        
        :param k: Int for k in calculating the country participation probability
        
        :param L: Int for L in calculating the country participation probability
        
        :return: An int for the discounted reward, an int for the country participation probability.

### Modeling 
For part 1 of the project, we constructed a world with different countries and implemented the simulation process for one country in terms of searching for different operations it can do in each step, and it was able to generate a schedule at last. In part 2, we expanded our settings for world modeling, including occurrences of wars as a new type of operator like TRANSFORM and TRANSFER and disasters as a type of intervention. For wars, we implemented the operator the BasicOperations.py file and the functions related to countries’ war incentives and inclinations in the country class of the Class.py. For disasters, we implemented the operation and outcomes of them in the InterventionManager.py. Both wars and disasters are called in Scheduler.py, where we implemented our gamer manager, in order to be incorporated in the game simulation. 

### Citation 
Cited group 1 for the idea of a need to define relationship score in warfare definition. 
Cited group 5 for the idea of using a double ended priority queue
Cited group 7 for definitions of TRANSFORM operations
