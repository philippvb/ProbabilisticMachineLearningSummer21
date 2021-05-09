import random
import copy
import time
import numpy as np
import matplotlib.pyplot as plt

class MCAgent:
    def __init__(self, ships, size, nb_samples=1000):
        self.nb_samples = nb_samples
        self.observed_board = np.zeros((size, size))
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
        n_samples = self.nb_samples

        #  +----------+
        #  |  Task 1  |
        #  +----------+
        # Check if there is already an "open" hit, i.e. a ship that has been hit but not sunk
        # These locations are handled by the observation_board as 1
        # If there is already a hit, choose a random one to deal with next.
        # Create a score board including that hit, and reduce the number of samples to 1/10
        hit = None
        if 1 in self.observed_board:
            hits = np.where(self.observed_board == 1)
            i = random.choice(range(len(hits[0])))
            hit = (hits[0][i], hits[1][i])
            n_samples /= 10

        #  +----------+
        #  |  Task 2  |
        #  +----------+
        # Populate the score_board with possible boat placements
        i = 0
        while i < n_samples:
            board = np.zeros_like(self.observed_board)
            for boat_size in self.remaining_ships:
                while True:
                    o = random.choice(['h', 'v'])
                    x = random.choice(range(self.size - (boat_size - 1 if o == 'h' else 0)))
                    y = random.choice(range(self.size - (boat_size - 1 if o == 'v' else 0)))

                    d = np.hstack((np.zeros((boat_size, 1)), np.arange(boat_size)[:, None])[::(-1 if o == 'h' else 1)])
                    boat = tuple((np.array([[x, y]]) + d).astype(int).T)

                    # Place boats non-overlapping and not on misses or sunken ships.
                    if 1 in board[boat] or -1 in self.observed_board[boat]:
                        continue

                    board[boat] = 1
                    break

            # Sanity check
            assert board.sum() == sum(self.remaining_ships)

            if not hit or board[hit] == 1:
                i += 1
                score_board += board

        #  +----------+
        #  |  Task 3  |
        #  +----------+
        # Having populated the score board, select a new position by choosing the location with the highest score.
        score_board *= np.where(self.observed_board == 1, 0, 1)
        plt.imshow(score_board, cmap='hot')
        plt.show()
        time.sleep(1)
        i_new, j_new = np.unravel_index(np.argmax(score_board), score_board.shape)

        # return the next location to query, i_new: int, j_new: int
        return i_new, j_new, score_board

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
