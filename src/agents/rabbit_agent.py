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


class RabbitAgent(Agent):
    def __init__(self, aid, initial_position, game_agent):
        super(RabbitAgent, self).__init__(aid=aid)

        display_message(self.aid.getLocalName(), "Creating RabbitAgent")

        self.position = initial_position
        self.hunger = 0
        self.game_type = GameConstants.RABBIT
        self.game_agent = game_agent

        self.alive = True

        self.additional_behaviours = [
            CallOnTimeBehaviour(self, 0.5, self.update),
            MovementBehaviour(self, self._build_message_for_proposer(), 7, 1, GameConstants.CARROT, GameConstants.RABBIT)
        ]

        for behaviour in self.additional_behaviours:
            self.behaviours.append(behaviour)

    def _build_message_for_proposer(self):
        message = ACLMessage(ACLMessage.CFP)
        message.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)

        message.add_receiver(self.game_agent.aid)

        return message

    def launch_contract_net_protocol(self):
        display_message(self.aid.getLocalName(), "Running RabbitAgent.launch")
        self.additional_behaviours[1].replace_message(self._build_message_for_proposer())
        self.call_later(0.1, self.additional_behaviours[1].on_start)


    def die(self):

        display_message(self.aid.localname, 'Asking GameAgent to KILL Rabbit')

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

    def update(self):
        if self.hunger >= 1:
            self.alive = False

        if not self.alive:
            self.die()
            #self.pause_agent()
        else:
            self.hunger += 1

            display_message(self.aid.getLocalName(), "Running RabbitAgent.update")
            display_message(self.aid.getLocalName(), f'Rabbit Hunger {self.hunger}')

            self.launch_contract_net_protocol()
