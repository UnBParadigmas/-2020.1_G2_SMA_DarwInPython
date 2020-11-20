from pade.behaviours.protocols import TimedBehaviour


class CallOnTimeBehaviour(TimedBehaviour):

    def __init__(self, agent, time, to_call):

        self.callable = to_call
        self._run = True

        super(CallOnTimeBehaviour, self).__init__(agent, time)

    def on_time(self):

        self.callable()

        if self._run:
            super(CallOnTimeBehaviour, self).on_time()

    def stop(self):
        self._run = False