from sys import set_asyncgen_hooks
from pade.misc.common import PadeSession
from pade.misc.utility import start_loop
from twisted.internet import reactor

class DarwInPython:

    instance: 'DarwInPython' = None

    def __init__(self):

        if DarwInPython.instance is None:
            DarwInPython.instance = self

            self.agents = list()
            self._loop_started = False

        else:
            raise Exception("DarwInPython already exists!")

    def run(self):
        self._loop_started = True
        start_loop(self.agents)

    @staticmethod
    def add_agent_to_loop(agent):

        if  DarwInPython.instance._loop_started:
            agent.update_ams(agent.ams)
            agent.on_start()
            ILP = reactor.listenTCP(agent.aid.port, agent.agentInstance)
            agent.ILP = ILP

        DarwInPython.instance.agents.append(agent)

