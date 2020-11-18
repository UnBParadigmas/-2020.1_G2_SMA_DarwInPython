from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.misc.utility import display_message

from behaviours.call_on_time import CallOnTimeBehaviour

from game.render import Render
from game.board import Board


class GameAgent(Agent):
    
    def __init__(self, aid):
        super(GameAgent, self).__init__(aid=aid)

        display_message(self.aid.getLocalName(), "Creating GameAgent.update")
        
        self.board = Board()
        self.render = Render()



    def update(self):

        display_message(self.aid.getLocalName(), "Running GameAgent.update")

        self.render.draw(self.board)
