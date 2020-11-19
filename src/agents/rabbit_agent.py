from pade.behaviours.protocols import Behaviour
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.misc.utility import display_message

from behaviours.call_on_time import CallOnTimeBehaviour
from behaviours.movement_behaviour import MovementBehaviour
from game.game_contants import GameConstants
from pade.acl.messages import ACLMessage


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
            MovementBehaviour(self, self._build_message_for_proposer())
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
        self.call_later(1.0, self.additional_behaviours[1].on_start)

    def update(self):
        display_message(self.aid.getLocalName(), "Running RabbitAgent.update")
        self.launch_contract_net_protocol()
