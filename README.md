# CS4269 Group4 Project
### Project Overview

### Setup For A simulation
We simulate a world of N virtual countries, each with M resources and some amount of each resource, including possibly zero units of some resources.

Files needed: 
      - BasicOperations.py
      - Classes.py
      - ReadInFile.py
      - ReadResources.py
      - Resources.py
      - ResourceQuality.py
      - Scheduler.py

Driver code:
      - Scheduler.py : 

- Clone or download a zip file for the project
- open terminal and cd into the project directory
- type in Scheduler.py to run the simulation 


### State Quality Function

The state quality is defined as the sum of the resource qualities for each resource a country possesses in a given state. 

Resource qualities are defined as the output of specific piecewise functions. Three functions exist (one for raw materials, one for produced materials, and one for waste).

- Raw Materials - Raw materials are modeled as having a linear slope until a minimum amount (called threshold of necessity) is possessed, then a linear but steeper slope until a limit (called threshold of saturation) is reached, before finally being modeled as a logarithmic curve.

- Produced Materials - Produced materials are modeled as having exponentially growing value until a minimum amount (called threshold of necessity) is possessed, then a linear slope until a limit (called threshold of saturation) is reached, before finally being modeled as a logarithmic curve.

- Waste - Wastes are modeled as having a linear slope until a minimum amount (called threshold of saturation) is possessed, then a linear but steeper slope thereafter.

### Successor Function

### Search Algorithm 

The search algorithm is A* search. Currently we only use the (state utility - current utility) to guide the search; no separate heuristic is used. Therefore, the function is closer to a greedy algorithm than true A*.

### Test Cases
