from .statemachine import StateMachine
from .guineapig import GuineaPig, GuineaPigActive, GuineaPigPassive


def build_guinea_pig_machine():
    m = StateMachine(15, 2000)
    m.add_state("SLEEPING", GuineaPigPassive, [-20, 3, 1])
    m.add_state("AWAKE", GuineaPigActive, [5, 5, 2])
    m.add_state("THINKING", GuineaPigPassive, [1, 3, 1])
    m.add_state("EATING", GuineaPigActive, [5, -10, 4])
    m.add_state("DRINKING", GuineaPigActive, [5, 5, -80])
    m.add_state("WANDERING", GuineaPigActive, [10, 10, 5])
    return m


def simulate_guinea_pig():
    gp_machine = build_guinea_pig_machine()
    gp_machine.run(GuineaPig("SLEEPING", 20, 10, 10))
    gp_machine.stats()


if __name__ == "__main__":
    simulate_guinea_pig()
