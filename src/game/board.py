import threading
import random

from game.game_contants import GameConstants

class Board:

    SIZE = (30, 30)

    def __init__(self):

        self.grid = []

        for line in range(0, self.SIZE[0]):
            columns = []        
            for col in range(0, self.SIZE[1]):
                columns.append(GameConstants.GRASS)

            self.grid.append(columns)
