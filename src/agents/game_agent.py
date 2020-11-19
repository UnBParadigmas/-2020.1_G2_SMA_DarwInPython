from random import getrandbits
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.misc.utility import display_message, start_loop

from behaviours.call_on_time import CallOnTimeBehaviour

from game.render import Render
from game.board import Board
from game.game_contants import GameConstants
from agents.rabbit_agent import RabbitAgent
from behaviours.movement_behaviour import MovementProviderBehaviour
from app import DarwInPython

import random

class GameAgent(Agent):
    
    def __init__(self, aid):
        super(GameAgent, self).__init__(aid=aid)

        display_message(self.aid.getLocalName(), "Creating GameAgent")
        
        self.board = Board()
        self.render = Render()

        self._next_port = self.aid.getPort() + 1

        self.populate_board(
            inital_values = [
                (GameConstants.RABBIT, 2)
            ]
        )

        self.behaviours.append(CallOnTimeBehaviour(self, 0.1, self.update))
        self.behaviours.append(CallOnTimeBehaviour(self, 1, self.add_carrots))
        self.behaviours.append(MovementProviderBehaviour(self))

    def _get_next_port_number(self):
        
        next_port = self._next_port
        self._next_port += 1

        return next_port

    def populate_board(self, inital_values: list):
        
        # each element in inital_values is a tuple with: (GameConstant.TYPE, amount)
        for grid_type, amount in inital_values:
            for _ in range(0, amount):
                with self.board.lock:
                    position = self.board.get_valid_position()

                    if grid_type == GameConstants.RABBIT:
                        new_agent_port = self._get_next_port_number()
                        rabbit = RabbitAgent(
                            AID(name=f'rabbit_agent_{new_agent_port}@localhost:{new_agent_port}'),
                            position,
                            self
                        )
                        DarwInPython.add_agent_to_loop(rabbit)
                        
                    self.board.set_position(grid_type, *position)

    def add_carrots(self):
        self.populate_board([(GameConstants.CARROT, 1)])

    def update(self):

        # display_message(self.aid.getLocalName(), "Running GameAgent.update")

        # movement order:
        # wolf, rabbit
        # then:
        # generate carrots

        #self.populate_board([(GameConstants.CARROT, 1)])

        self.render.draw(self.board)
