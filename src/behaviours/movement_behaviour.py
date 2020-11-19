from random import randint
from pade.behaviours.protocols import TimedBehaviour
from pade.acl.messages import ACLMessage
from pade.behaviours.protocols import FipaContractNetProtocol
from pade.misc.utility import display_message

from game.board import Board

import pickle
import random
from time import time


class MovementBehaviour(FipaContractNetProtocol):
    
    def __init__(self, agent, message):
        super(MovementBehaviour, self).__init__(
            agent=agent, message=message, is_initiator=True)
        self.replace_message(message)

    def replace_message(self, message):
        self.cfp = message
        self.message = message
    
    def handle_all_proposes(self, proposes):

        super(MovementBehaviour, self).handle_all_proposes(proposes)

        if len(proposes) < 1:
            display_message(self.agent.aid.name, 'No PROPOSE Received')

        game_data = pickle.loads(proposes[0].content)

        display_message(
            self.agent.aid.name,
            f'Received game data: {game_data}'
        )

        size = (
            len(game_data['grid'][0]),
            len(game_data['grid'])
        )

        new_position = (
            self.agent.position[0] + 1 if self.agent.position[0] + 1 < size[0] else 0,
            self.agent.position[1]
        )
        
        response = {
            'caller_type': self.agent.game_type,
            'orginal_position': self.agent.position,
            'target_position': new_position
        }

        display_message(self.agent.aid.name,
                        f'Moving from {response["orginal_position"]} to {new_position}')

        self.agent.position = new_position
        
        answer = ACLMessage(ACLMessage.ACCEPT_PROPOSAL)
        answer.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
        answer.set_content(pickle.dumps(response))
        answer.add_receiver(proposes[0].sender)
        self.agent.send(answer)

    def handle_inform(self, message):
        super(MovementBehaviour, self).handle_inform(message)
        display_message(self.agent.aid.name, 'INFORM message received')

    def handle_refuse(self, message):
        super(MovementBehaviour, self).handle_refuse(message)
        display_message(self.agent.aid.name, 'REFUSE message received')

    def handle_propose(self, message):
        super(MovementBehaviour, self).handle_propose(message)
        display_message(self.agent.aid.name, 'PROPOSE message received')

class MovementProviderBehaviour(FipaContractNetProtocol):
   
    def __init__(self, agent):
        super(MovementProviderBehaviour, self).__init__(
            agent=agent,
            message=None,
            is_initiator=False
        )

    def handle_cfp(self, message):
        display_message(self.agent.aid.name, 'handle CFP - call later')
        self.agent.call_later(1.0, self._handle_cfp, message)

    def _handle_cfp(self, message):
        super(MovementProviderBehaviour, self).handle_cfp(message)
        self.message = message

        display_message(self.agent.aid.name, 'CFP message received')

        answer = self.message.create_reply()
        answer.set_performative(ACLMessage.PROPOSE)

        data = {
            'grid': self.agent.board.grid,
        }           

        answer.set_content(pickle.dumps(data))

        self.agent.send(answer)

    def handle_reject_propose(self, message):
        super(MovementProviderBehaviour, self).handle_reject_propose(message)
        display_message(self.agent.aid.name,
                        'REJECT_PROPOSAL message received')

    def handle_accept_propose(self, message):
        super(MovementProviderBehaviour, self).handle_accept_propose(message)
        display_message(self.agent.aid.name,
                        'ACCEPT_PROPOSE message received')
        
        content = ''
        data = pickle.loads(message.content)
        try:
            self.agent.board.execute_move(
                data['caller_type'],
                data['orginal_position'],
                data['target_position']
            )
            content = 'OK'
        except Exception as e:
            display_message(self.agent.aid.name,
                            f'EXCEPTION: {e}')
            content = 'ERROR'
            
        answer = message.create_reply()
        answer.set_performative(ACLMessage.INFORM)
        answer.set_content(content)
        self.agent.send(answer)


   
 
