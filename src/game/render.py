import pygame
from pygame.constants import SCRAP_SELECTION

from game.board import Board
from game.game_contants import GameConstants


class Render:
    
    SCREEN_SIZE = (600, 600)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

    def draw(self, board: Board):
        
        block_size = (
            self.SCREEN_SIZE[0] / board.SIZE[0],
            self.SCREEN_SIZE[1] / board.SIZE[1]
        )

        for x, line in enumerate(board.grid):
            for y, grid_object in enumerate(line):
                # Draw a solid blue circle in the center
                
                # TODO: change grid_type implementation
                grid_type = grid_object

                rect = pygame.Rect(x * block_size[0], y * block_size[1], *block_size)
                pygame.draw.rect(self.screen, GameConstants.COLORS[grid_type], rect)

        # Flip the display
        pygame.display.flip()
