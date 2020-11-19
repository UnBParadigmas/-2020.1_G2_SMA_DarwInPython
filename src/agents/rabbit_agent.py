from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.misc.utility import display_message

from behaviours.call_on_time import CallOnTimeBehaviour


class RabbitAgent(Agent):
    def __init__(self, aid, initial_position):
        super(Agent, self).__init__(aid=aid)

        display_message(self.aid.getLocalName(), "Creating RabbitAgent")
        
        self.position = initial_position
        self.hunger = 0

        self.alive = True

        call_behaviour = CallOnTimeBehaviour(self, 1.0, self.update)
        self.behaviours.append(call_behaviour)


    def update(self):
        display_message(self.aid.getLocalName(), "Running RabbitAgent.update")
