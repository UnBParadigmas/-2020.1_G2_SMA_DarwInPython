from pade.acl.messages import ACLMessage
from pade.behaviours.protocols import FipaContractNetProtocol
from pade.misc.utility import display_message

import pickle

class GameCommunicationInitiator(FipaContractNetProtocol):
   
    def __init__(self, agent, message):
        super(GameCommunicationInitiator, self).__init__(
            agent=agent, message=message, is_initiator=True)

        self.replace_message(message)

    def replace_message(self, message):
        # used to fix cases where the communication would stop,
        # restarts the message to an initial state
        self.cfp = message
        self.message = message

    def handle_all_proposes(self, proposes):

        super(GameCommunicationInitiator, self).handle_all_proposes(proposes)

        if len(proposes) < 1:
            display_message(self.agent.aid.name, 'No PROPOSE Received')

        self.handle_response(proposes[0])

    def get_response(self, message):
        raise NotImplementedError

    def reset_event(self, message):
        # should be overriden when its needed to undo an action
        # from handle_response in case of errors received on
        # handle_inform
        pass

    def confirm_event(self, message):
        # called when an success is received on the INFORM message
        pass

    def send_response(self, response, sender):
        
        answer = ACLMessage(ACLMessage.ACCEPT_PROPOSAL)
        answer.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
        answer.set_content(pickle.dumps(response))
        answer.add_receiver(sender)
        self.agent.send(answer)

    def handle_response(self, message):
        response = self.get_response(message)
        self.send_response(response, message.sender)

    def handle_inform(self, message):
        super(GameCommunicationInitiator, self).handle_inform(message)
        display_message(self.agent.aid.name, 'INFORM message received')

        data = pickle.loads(message.content)
        display_message(self.agent.aid.name, f'INFORM data: {data}')

        if data['msg'] != 'OK':
            self.reset_event(message)

            # data always has the 'msg' key, if there is
            # another key, its data for the rerun of this
            # communication protocol
            if len(data.keys()) > 1:
                self.handle_response(message)
        else:
            self.confirm_event(message)

    def handle_refuse(self, message):
        super(GameCommunicationInitiator, self).handle_refuse(message)
        display_message(self.agent.aid.name, 'REFUSE message received')

    def handle_propose(self, message):
        super(GameCommunicationInitiator, self).handle_propose(message)
        display_message(self.agent.aid.name, 'PROPOSE message received')



class GameCommunicationParticipant(FipaContractNetProtocol):

    def __init__(self, agent):
        super(GameCommunicationParticipant, self).__init__(
            agent=agent,
            message=None,
            is_initiator=False
        )

    def handle_cfp(self, message):
        display_message(self.agent.aid.name, 'handle CFP - call later')
        self.agent.call_later(1.0, self._handle_cfp, message)

    def _handle_cfp(self, message):
        super(GameCommunicationParticipant, self).handle_cfp(message)
        self.message = message

        display_message(self.agent.aid.name, 'CFP message received')

        answer = self.message.create_reply()
        answer.set_performative(ACLMessage.PROPOSE)
        content = self.get_cfp_content(message)
        answer.set_content(pickle.dumps(content))

        self.agent.send(answer)

    def get_cfp_content(self, message):
        raise NotImplementedError

    def handle_reject_propose(self, message):
        super(GameCommunicationParticipant, self).handle_reject_propose(message)
        display_message(self.agent.aid.name,
                        'REJECT_PROPOSAL message received')

    def create_inform_message(self, message):
        raise NotImplementedError

    def handle_accept_propose(self, message):
        super(GameCommunicationParticipant, self).handle_accept_propose(message)
        display_message(self.agent.aid.name,
                        'ACCEPT_PROPOSE message received')

        content = self.create_inform_message(message)

        answer = message.create_reply()
        answer.set_performative(ACLMessage.INFORM)
        answer.set_content(pickle.dumps(content))
        self.agent.send(answer)