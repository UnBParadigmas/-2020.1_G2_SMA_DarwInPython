from random import getrandbits
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.misc.utility import display_message

from behaviours.call_on_time import CallOnTimeBehaviour

from game.render import Render
from game.board import Board
from game.game_contants import GameConstants

import random


class GameAgent(Agent):
    
    def __init__(self, aid):
        super(GameAgent, self).__init__(aid=aid)

        display_message(self.aid.getLocalName(), "Creating GameAgent")
        
        self.board = Board()
        self.render = Render()

        self.populate_board(
            inital_values = [
                (GameConstants.RABBIT, 2)
            ]
        )

        call_behaviour = CallOnTimeBehaviour(self, 1.0, self.update)
        self.behaviours.append(call_behaviour)

    def populate_board(self, inital_values: list):
        
        # each element in inital_values is a tuple with: (GameConstant.TYPE, amount)
        for grid_type, amount in inital_values:
            for _ in range(0, amount):
                position = self.board.get_valid_position()
                # TODO: instantiate agent
                self.board.grid[position[0]][position[1]] = grid_type

    def update(self):

        display_message(self.aid.getLocalName(), "Running GameAgent.update")

        # movement order:
        # wolf, rabbit
        # then:
        # generate carrots

        self.populate_board([(GameConstants.CARROT, 1)])

        self.render.draw(self.board)
