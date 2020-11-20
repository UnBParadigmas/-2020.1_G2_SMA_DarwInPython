from pade.behaviours.protocols import Behaviour
from pade.behaviours.protocols import FipaRequestProtocol
from pade.misc.utility import display_message

from app import DarwInPython
from game.game_contants import GameActions, GameConstants
import pickle 

class RemoveAgentBehaviour(FipaRequestProtocol):

    def __init__(self, agent):
        super(RemoveAgentBehaviour, self).__init__(agent=agent,
                                          message=None,
                                          is_initiator=False)

    def execute(self, message):
        self.remove_agent(message)

    def remove_agent(self, message):

        #display_message(self.agent.aid.getLocalName(), f"RemoveAgenteBehaviour called: {message}")

        message_content = None
        try:
            message_content = pickle.loads(message.content)
            # display_message(self.agent.aid.getLocalName(), f"Received SUCCESS ON PICKLE: {message_content}")
        except TypeError as e:
            #display_message(self.aid.getLocalName(), "Received TYPE ERROR")
            return


        display_message(self.agent.aid.getLocalName(), f"content: {message_content}")
        if 'action' in message_content.keys():
            display_message(self.agent.aid.getLocalName(), f"ACTION is {message_content['action']}")
            if message_content['action'] == GameActions.KILL:

                display_message(self.agent.aid.getLocalName(), f"Received KILL command: {message_content}")

                position = message_content['position']
                port = message_content['port']
                game_type = message_content['game_type']

                with self.agent.board.lock:
                    if self.agent.board.get_position(*position) == game_type:
                        self.agent.board.set_position(GameConstants.GRASS, *position)

                    DarwInPython.remove_agent_from_loop(port)
