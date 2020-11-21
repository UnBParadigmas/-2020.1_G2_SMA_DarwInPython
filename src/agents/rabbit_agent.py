from game.game_contants import GameConstants
from agents.animal_agent import AnimalAgent

class RabbitAgent(AnimalAgent):
    def __init__(self, aid, initial_position, game_agent):
        super(RabbitAgent, self).__init__(
            aid=aid,
            initial_position=initial_position,
            game_agent=game_agent,
            game_type=GameConstants.RABBIT,
            food_type=GameConstants.CARROT,
        )
        self.vision_distance = 10
        self.hunger_limit = 60
        self.max_hunger = 30
        self.hunger = self.max_hunger - 5
