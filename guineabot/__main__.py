import logging

from .statemachine import StateMachine
from .guineapig import GuineaPig, GuineaPigState


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def build_guinea_pig_machine():
    sm = StateMachine(15, 2000)
    sm.add_state("SLEEPING", GuineaPigState, [-20, 3, 1])
    sm.add_state("AWAKE", GuineaPigState, [5, 5, 2])
    sm.add_state("THINKING", GuineaPigState, [1, 3, 1])
    sm.add_state("EATING", GuineaPigState, [5, -10, 4])
    sm.add_state("DRINKING", GuineaPigState, [5, 5, -80])
    sm.add_state("WANDERING", GuineaPigState, [10, 10, 5])
    return sm


def simulate_guinea_pig():
    logging.info("Booting guinea pig...")
    gp_machine = build_guinea_pig_machine()
    a_guinea_pig = GuineaPig("SLEEPING", 20, 10, 10)
    logging.info("It's alive!")
    gp_machine.run(a_guinea_pig)
    gp_machine.stats()


if __name__ == "__main__":
    simulate_guinea_pig()
