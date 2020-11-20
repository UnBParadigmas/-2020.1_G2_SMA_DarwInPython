from sys import set_asyncgen_hooks
from pade.misc.common import PadeSession
from pade.misc.utility import start_loop
from twisted.internet import reactor

from threading import Lock

class DarwInPython:

    instance: 'DarwInPython' = None

    def __init__(self):

        if DarwInPython.instance is None:
            DarwInPython.instance = self

            self.agents = list()
            self._agents_lock = Lock()
            self._loop_started = False


        else:
            raise Exception("DarwInPython already exists!")

    def run(self):
        self._loop_started = True
        start_loop(self.agents)

    @staticmethod
    def add_agent_to_loop(agent):

        with  DarwInPython.instance._agents_lock:

            if  DarwInPython.instance._loop_started:
                agent.update_ams(agent.ams)
                agent.on_start()
                ILP = reactor.listenTCP(agent.aid.port, agent.agentInstance)
                agent.ILP = ILP

            DarwInPython.instance.agents.append(agent)

    @staticmethod
    def remove_agent_from_loop(agent_port, tries=0):

        if tries > 3:
            return

        error = False
        with  DarwInPython.instance._agents_lock:
            index_to_remove = None

            for idx, search_agent in enumerate(DarwInPython.instance.agents):
                if agent_port == search_agent.aid.port:
                    index_to_remove = idx
                    break

            if index_to_remove is not None:
                if agent_port == DarwInPython.instance.agents[index_to_remove].aid.port:
                    DarwInPython.instance.agents.pop(index_to_remove)
                else:
                    error = True

        if error:
            DarwInPython.remove_agent_from_loop(agent_port, tries=tries + 1)

