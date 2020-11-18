
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv

from agents.game_agent import GameAgent


if __name__ == '__main__':

    agents_per_process = 1
    c = 0

    agents = list()

    for i in range(agents_per_process):

        port = int(argv[1]) + c

        game_agent = GameAgent(AID(name=f'game_agent_{port}@localhost:{port}'))
        agents.append(game_agent)

        c += 1000

    start_loop(agents)
