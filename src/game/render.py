import pygame

from game.board import Board


class Render:
    
    SCREEN_SIZE = (600, 600)
    GRID_BLOCK_SIZE = (20, 20)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

    def draw(self, board: Board):

        for x, line in enumerate(board.grid):
            for y, col in enumerate(line):
                # Draw a solid blue circle in the center
                rect = pygame.Rect(x * self.GRID_BLOCK_SIZE[0], y * self.GRID_BLOCK_SIZE[1], *self.GRID_BLOCK_SIZE)
                pygame.draw.rect(self.screen, (0, 0, x+y), rect)

        # Flip the display
        pygame.display.flip()
