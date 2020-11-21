from pade.behaviours.protocols import Behaviour
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.misc.utility import display_message
from pade.acl.messages import ACLMessage

from behaviours.call_on_time import CallOnTimeBehaviour
from behaviours.movement_behaviour import MovementBehaviour
from game.game_contants import GameConstants, GameActions
from pade.acl.messages import ACLMessage

import pickle


class AnimalAgent(Agent):
    def __init__(self, aid, initial_position, game_agent, game_type, food_type):
        super(AnimalAgent, self).__init__(aid=aid)

        self.position = initial_position
        self.hunger = 0
        self.game_agent = game_agent

        self.game_type = game_type
        self.food_type = food_type
        self.vision_distance = 10
        self.hunger_limit = 60
        self.max_hunger = 30

        self.alive = True

        self.additional_behaviours = [
            CallOnTimeBehaviour(self, 0.5, self.update),
            MovementBehaviour(
                self,
                self._build_message_for_proposer(),
                1,
                self.food_type,
                self.game_type
            )
        ]

        for behaviour in self.additional_behaviours:
            self.behaviours.append(behaviour)

    def _build_message_for_proposer(self):
        message = ACLMessage(ACLMessage.CFP)
        message.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)

        message.add_receiver(self.game_agent.aid)

        return message

    def launch_contract_net_protocol(self):
        self.additional_behaviours[1].replace_message(self._build_message_for_proposer())
        self.call_later(0.1, self.additional_behaviours[1].on_start)


    def die(self):

        message = ACLMessage(ACLMessage.INFORM)
        message.add_receiver(self.game_agent.aid)
        content = {
            'port': self.aid.port,
            'position': self.position,
            'game_type': self.game_type,
            'action': str(GameActions.KILL)
        }
        message.set_content(pickle.dumps(content))

        self.send(message)
        self.call_later(3, self.additional_behaviours[0].stop)

    def update(self):
        if self.hunger >= self.hunger_limit:
            self.alive = False

        if not self.alive:
            self.call_later(0.5, self.die)
        else:
            self.hunger += 1

            self.launch_contract_net_protocol()
