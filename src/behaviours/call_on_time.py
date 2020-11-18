from pade.behaviours.protocols import TimedBehaviour


class CallOnTimeBehaviour(TimedBehaviour):

    def __init__(self, agent, time, to_call):

        self.callable = to_call

        super(CallOnTimeBehaviour, self).__init__(agent, time)

    def on_time(self):

        self.callable()
        super(CallOnTimeBehaviour, self).on_time()
