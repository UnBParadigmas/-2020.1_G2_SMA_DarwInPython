import threading
import random

from game.game_contants import GameConstants
from game.exceptions import InvalidMovementException


class Board:

    SIZE = (30, 30)

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

    def get_valid_position(self):

        rand_pos = self._get_rand_pos()
        while self.get_position(*rand_pos) != GameConstants.GRASS:
            rand_pos = self._get_rand_pos()

        return rand_pos

    def validate_type(self, caller_type, original_position):
        if caller_type != self.get_position(*original_position):
            raise InvalidMovementException()

    def validate_movement(self, caller_type, original_position, target_position):
        self.validate_type(caller_type, original_position)
        target_position_type = self.get_position(*target_position)
        if caller_type == GameConstants.RABBIT and \
            target_position_type not in [GameConstants.GRASS, GameConstants.CARROT]:

            raise InvalidMovementException()

    def execute_move(self, caller_type, original_position, target_position):

        with self.lock:
            self.validate_movement(caller_type, original_position, target_position)

            self.set_position(GameConstants.GRASS, *original_position)
            self.set_position(caller_type, *target_position)