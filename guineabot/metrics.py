from typing import List

from prometheus_client import Enum, Gauge, Info


class Metrics:

    def __init__(self, states: List[str]) -> None:
        """
        Initialise the metric holders.
        :param states: the guinea pig can be in
        """
        self.info = Info('guineapig', 'About the guinea-pig')
        self.current_age = Gauge('guineapig_age', 'How old the guinea-pig is')
        self.state = Enum('guineapig_state', 'What the guinea-pig is currently doing', states=states)
        self.tired = Gauge('guineapig_tired', 'How tired the guinea-pig is')
        self.hunger = Gauge('guineapig_hunger', 'How hungry the guinea pig is')
        self.thirst = Gauge('guineapig_thirst', 'How thirsty the guinea pig is')

    def publish(self, internal_state: dict) -> None:
        """
        Update the metrics.
        """
        self.info.info({'name': internal_state['name']})
        self.current_age.set(internal_state['current_age'])
        self.state.state(internal_state['state'])
        self.tired.set(internal_state['tired'])
        self.hunger.set(internal_state['hunger'])
        self.thirst.set(internal_state['thirst'])
