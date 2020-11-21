import pygame
from pygame.constants import SCRAP_SELECTION

from game.board import Board
from game.game_contants import GameConstants
import sys

class Render:
    
    SCREEN_SIZE = (800, 800)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

    def draw(self, board: Board):
        
        block_size = (
            int(self.SCREEN_SIZE[0] / board.SIZE[0]),
            int(self.SCREEN_SIZE[1] / board.SIZE[1])
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # you have to reference event.type in this for loop
                pygame.quit()
                sys.exit()

        for x, line in enumerate(board.grid):
            for y, grid_object in enumerate(line):

                grid_type = grid_object

                rect = pygame.Rect(x * block_size[0], y * block_size[1], *block_size)
                pygame.draw.rect(self.screen, GameConstants.COLORS[grid_type], rect)

        # Flip the display
        pygame.display.flip()
