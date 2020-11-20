from random import getrandbits
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message, start_loop

from behaviours.call_on_time import CallOnTimeBehaviour

from game.render import Render
from game.board import Board
from game.game_contants import GameConstants, GameActions
from agents.rabbit_agent import RabbitAgent
# from agents.wolf_ import RabbitAgent
from behaviours.movement_behaviour import MovementProviderBehaviour
from behaviours.remove_agent_behaviour import RemoveAgentBehaviour
from app import DarwInPython

import random
import pickle
from pickle import dumps, loads

class GameAgent(Agent):
    
    def __init__(self, aid):
        super(GameAgent, self).__init__(aid=aid)

        display_message(self.aid.getLocalName(), "Creating GameAgent")
        
        self.board = Board()
        self.render = Render()

        self._next_port = self.aid.getPort() + 1

        self.populate_board(
            inital_values = [
                (GameConstants.RABBIT, 10)
            ]
        )

        self.behaviours.append(CallOnTimeBehaviour(self, 0.1, self.update))
        self.behaviours.append(RemoveAgentBehaviour(self))
        self.behaviours.append(CallOnTimeBehaviour(self, 1, self.add_carrots))
        self.behaviours.append(MovementProviderBehaviour(self))

    def react(self, message):

        if message.system_message:
            for system_behaviour in self.system_behaviours:
                system_behaviour.execute(message)
        else:
            for behaviour in self.behaviours:
                #display_message(self.aid.getLocalName(), f"Sending message {message} to Behaviour: {behaviour}")
                behaviour.execute(message)

        if 'ams' not in message.sender.name and 'sniffer' not in self.aid.name:
            # sends the received message to Sniffer
            # building of the message to be sent to Sniffer.
            _message = ACLMessage(ACLMessage.INFORM)
            sniffer_aid = AID('sniffer@' + self.sniffer['name'] + ':' + str(self.sniffer['port']))
            _message.add_receiver(sniffer_aid)
            _message.set_content(dumps({
            'ref' : 'MESSAGE',
            'message' : message}))
            _message.set_system_message(is_system_message=True)
            self.send(_message)


    def _get_next_port_number(self):
        
        next_port = self._next_port
        self._next_port += 1

        return next_port

    def spawn_agent_close_to_position(self, agent_type, center_position):
        
        with self.board.lock:
            
            position = self.board.get_valid_position(center_position)
            
            if position is None:
                return

            self.spawn_agent(agent_type, position)
        
         
    def spawn_agent(self, agent_type, position):
        
        if agent_type == GameConstants.RABBIT:

            new_agent_port = self._get_next_port_number()
          
            rabbit = RabbitAgent(
                AID(name=f'rabbit_agent_{new_agent_port}@localhost:{new_agent_port}'),
                position,
                self
            )
          
            DarwInPython.add_agent_to_loop(rabbit)

        self.board.set_position(agent_type, *position)

    def populate_board(self, inital_values: list):
        
        # each element in inital_values is a tuple with: (GameConstant.TYPE, amount)
        for grid_type, amount in inital_values:
            for _ in range(0, amount):
                with self.board.lock:
                    position = self.board.get_random_position()
                    
                    self.spawn_agent(grid_type, position)


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
