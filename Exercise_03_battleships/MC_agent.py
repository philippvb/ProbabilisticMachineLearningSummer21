import random
import copy
from IPython.lib.display import ScribdDocument
import numpy as np

class MCAgent:

    def __init__(self, ships, size, nb_samples = 1000):
        self.nb_samples = nb_samples
        self.observed_board = np.zeros((size,size))
        self.remaining_ships = ships
        self.size = size

    def select_observation(self):
        """
        --------------------------------------------------
        THIS IS THE MONTE CARLO SAMPLER YOU NEED TO ADAPT.
        --------------------------------------------------
        
        Select the next location to be observed
        :returns: i_new: int, j_new: int
        """
        
        # New board to collect the states sampled by the MC agent
        score_board = np.zeros_like(self.observed_board)
        
        #  +----------+
        #  |  Task 1  |
        #  +----------+
        # Check if there is already an "open" hit, i.e. a ship that has been hit but not sunk
        # These locations are handled by the observation_board as 1

    

        

            
        #  +------------+
        #  |  Task 1a)  |
        #  +------------+
        # If there is already a hit, choose a random one to deal with next.
        # Create a score board including that hit, and reduce the number of samples to 1/10
        indices_x, indices_y = np.where(self.observed_board == 1)
        if indices_x.shape[0] > 0:
            for i in range(int(self.nb_samples/10)):
                random_index = np.random.randint(0, indices_x.shape[0])
                hit_x = indices_x[random_index]
                hit_y = indices_y[random_index]
                        
            #  +----------+
            #  |  Task 2  |
            #  +----------+
            # Populate the score_board with possible boat placements
                for boat_length in self.remaining_ships:
                    max_x_index = min([hit_x, self.observed_board.shape[0] - boat_length+1])
                    for x in range(hit_x - boat_length+1, max_x_index+1):
                        if -1 not in self.observed_board[x:x+boat_length, hit_y]: # valid position
                            score_board[x:x+boat_length, hit_y]+=1 # vertical
                    max_y_index = min([hit_y, self.observed_board.shape[1] - boat_length+1])
                    for y in range(hit_y - boat_length+1, max_y_index+1):
                        if -1 not in self.observed_board[hit_x, y:y+boat_length]: # valid position
                            score_board[hit_x, y:y+boat_length]+=1 # horizontal

            # now set already hits to 0
            score_board[np.where(self.observed_board == 1)] = 0
            
            # if no open hit left, go through whole board to compute posterior 
        else:
            for boat_length in self.remaining_ships:
                for x in range(self.observed_board.shape[0]-boat_length+1):
                    for y in range(self.observed_board.shape[1]):
                        if -1 not in self.observed_board[x:x+boat_length, y]: # valid position
                            score_board[x:x+boat_length, y]+=1 # vertical
                        

                for y in range(self.observed_board.shape[1]-boat_length+1):
                    for x in range(self.observed_board.shape[0]):
                        if -1 not in self.observed_board[x, y:y+boat_length]: # valid position
                            score_board[x, y:y+boat_length]+=1 # horizontal

        




        #  +----------+
        #  |  Task 3  |
        #  +----------+
        # Having populated the score board, select a new position by choosing the location with the highest score.
        max_x, max_y = np.unravel_index(np.argmax(score_board, axis=None), score_board.shape)
        # return the next location to query, i_new: int, j_new: int
        return max_x, max_y, score_board
#         return i_new, j_new
    
    def update_observations(self, i, j, observation, sunken_ship):
        if observation:
            self.observed_board[i,j] = 1
        else:
            self.observed_board[i,j] = -1
        if not sunken_ship is None:
            i,j,l,h = sunken_ship
            self.remaining_ships.remove(l)
            if h:
                self.observed_board[i,j:j+l] = -1
            else:
                self.observed_board[i:i+l,j] = -1
