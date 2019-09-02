from statemachine import StateMachine
import random


class GuineaPig:

    def __init__(self, tired, hunger, thirst):
        self.tired = tired
        self.hunger = hunger
        self.thirst = thirst

    def is_tired(self, state):
        # We won't sleep if we are hungry or thirsty.
        if self.is_hungry(state) or self.is_thirsty():
            return False
        if state == "SLEEPING":
            # If we are already sleeping, carry on sleeping.
            return self.tired > 30
        else:
            return self.tired > 80

    def is_hungry(self, state):
        # We won't eat if we are thirsty.
        if self.is_thirsty():
            return False
        if state == "EATING":
            # If already eating, keep on eating.
            return self.hunger > 30
        else:
            return self.hunger > 80

    def is_thirsty(self):
        return self.thirst > 80

    @staticmethod
    def outside_bounds(attribute):
        return attribute < 0 or attribute > 130

    def apply_changes(self, changes):
        self.tired += changes[0]
        self.hunger += changes[1]
        self.thirst += changes[2]
        if self.outside_bounds(self.tired) or self.outside_bounds(self.hunger) or self.outside_bounds(self.thirst):
            print("Rogue: " + str(self))
            raise OverflowError

    def __str__(self):
        return "GuineaPig:(Hunger: {0}, Thirst:{1}, Tired:{2})".format(self.hunger, self.thirst, self.tired)


class State:

    def __init__(self, state, changes):
        self.state = state
        self.changes = changes

    def transition(self, gp: GuineaPig):
        pass


class Passive(State):

    def __init__(self, state, changes):
        super(Passive, self).__init__(state, changes)

    def transition(self, gp: GuineaPig):
        gp.apply_changes(self.changes)
        if not gp.is_tired(self.state):
            new_state = "AWAKE"
        elif random.randint(1, 10) > 8:
            new_state = "STANDBY"
        else:
            new_state = "SLEEPING"
        return new_state, gp


class Active(State):

    def __init__(self, state, changes):
        super(Active, self).__init__(state, changes)

    def transition(self, gp: GuineaPig):
        gp.apply_changes(self.changes)
        if gp.is_tired(self.state):
            new_state = "SLEEPING"
        elif gp.is_hungry(self.state):
            new_state = "EATING"
        elif gp.is_thirsty():
            new_state = "DRINKING"
        elif random.randint(1, 10) > 8:
            new_state = "WANDERING"
        elif random.randint(1, 10) > 1:
            new_state = "STANDBY"
        else:
            new_state = "AWAKE"
        return new_state, gp


if __name__ == "__main__":
    m = StateMachine()
    m.add_state("SLEEPING", Passive, [-20, 3, 1])
    m.add_state("AWAKE", Active, [5, 5, 2])
    m.add_state("STANDBY", Passive, [1, 3, 1])
    m.add_state("EATING", Active, [5, -10, 4])
    m.add_state("DRINKING", Active, [5, 5, -80])
    m.add_state("WANDERING", Active, [10, 10, 5])
    m.run("SLEEPING", GuineaPig(20, 10, 10), 2000, 15)
