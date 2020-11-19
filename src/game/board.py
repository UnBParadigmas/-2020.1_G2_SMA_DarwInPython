import threading
import random

from game.game_contants import GameConstants
from game.exceptions import InvalidMovementException


class Board:

    SIZE = (30, 30)

    def __init__(self):

        self.grid = []
        self.lock = threading.Lock()
        self._current_locking_id = 0
        self._next_locking_id = 1

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

    def acquire_board_lock(self):
        self.lock.acquire()
        return 0

    def release(self, lock_id):
        self.lock.release()
        pass

    def execute_move(self, lock_id, caller_type, original_position, target_position):

        self.validate_movement(caller_type, original_position, target_position)

        self.set_position(GameConstants.GRASS, *original_position)
        self.set_position(caller_type, *target_position)

        self.release(lock_id)

            
            
            