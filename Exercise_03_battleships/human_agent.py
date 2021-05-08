import random
import copy
import numpy as np

class HumanAgent:

    def __init__(self):
        pass

    def select_observation(self):
        i = input('Enter row coordinate: ')
        j = input('Enter column coordinate: ')
        return int(i),int(j), None

    def update_observations(self,i,j,observation, sunken_ship):
        pass
