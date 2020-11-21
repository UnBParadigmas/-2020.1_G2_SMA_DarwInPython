import threading
import random
import itertools

from game.game_contants import GameConstants
from game.exceptions import InvalidMovementException, InvalidMovementTargetException, InvalidMovimentOriginException


class Board:

    SIZE = (70, 70)

    def __init__(self):

        self.grid = []
        self.lock = threading.Lock()

        for line in range(0, self.SIZE[0]):
            columns = []
            for col in range(0, self.SIZE[1]):
                columns.append(GameConstants.GRASS)

            self.grid.append(columns)

    def _get_rand_pos(self):
        return (
            random.randint(0, self.SIZE[0] - 1),
            random.randint(0, self.SIZE[1] - 1)
        )

    def get_position(self, x, y):
        return self.grid[x][y]

    def set_position(self, game_type, x, y):
        self.grid[x][y] = game_type

    def get_random_position(self):

        rand_pos = self._get_rand_pos()
        while self.get_position(*rand_pos) != GameConstants.GRASS:
            rand_pos = self._get_rand_pos()

        return rand_pos

    def get_valid_position(self, position):
        all_combinations = []
        for i in range(position[0] - 1, position[0] + 2):
            for j in range(position[1] - 1, position[1] + 2):
                all_combinations.append((i, j))
        

        selected_position = None
        for possible_position in all_combinations:

            if not (
                0 <= possible_position[0] < self.SIZE[0] \
                and 0 <= possible_position[1] < self.SIZE[1]
            ):
                continue

            target_position_type = self.get_position(*possible_position)
            if target_position_type == GameConstants.GRASS:
                selected_position = possible_position
                break
        
        return selected_position
        

    def validate_type(self, caller_type, original_position):
        if caller_type != self.get_position(*original_position):
            raise InvalidMovimentOriginException()

    def validate_movement(self, caller_type, original_position, target_position):
        self.validate_type(caller_type, original_position)
        target_position_type = self.get_position(*target_position)
        if caller_type == GameConstants.RABBIT and \
            target_position_type not in [GameConstants.GRASS, GameConstants.CARROT]:

            raise InvalidMovementTargetException()

    def execute_move(self, caller_type, original_position, target_position):

        old_grid_value = None
        with self.lock:
            self.validate_movement(caller_type, original_position, target_position)
            
            old_grid_value = self.get_position(*target_position) 

            self.set_position(GameConstants.GRASS, *original_position)
            self.set_position(caller_type, *target_position)

        return old_grid_value

