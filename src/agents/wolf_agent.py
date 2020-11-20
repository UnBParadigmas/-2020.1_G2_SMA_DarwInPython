from game.game_contants import GameConstants
from agents.animal_agent import AnimalAgent


class WolfAgent(AnimalAgent):
    def __init__(self, aid, initial_position, game_agent):
        super(WolfAgent, self).__init__(
            aid=aid,
            initial_position=initial_position,
            game_agent=game_agent,
            game_type=GameConstants.WOLF,
            food_type=GameConstants.RABBIT,
            vision_distance=15
        )
        