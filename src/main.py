
from pade.acl.aid import AID
from sys import argv

from agents.game_agent import GameAgent
from app import DarwInPython

if __name__ == '__main__':

    app = DarwInPython()
    
    port = int(argv[1])

    game_agent = GameAgent(AID(name=f'game_agent_{port}@localhost:{port}'))
    DarwInPython.add_agent_to_loop(game_agent)
    
    app.run()
