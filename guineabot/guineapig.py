from statemachine import StateMachine
import random


class GuineaPig:

    def __init__(self, state, tired, hunger, thirst):
        self.state = state.upper()
        self.tired = tired
        self.hunger = hunger
        self.thirst = thirst

    def is_tired(self):
        # We won't sleep if we are hungry or thirsty.
        if self.is_hungry() or self.is_thirsty():
            return False
        if self.state == "SLEEPING":
            # If we are already sleeping, carry on sleeping.
            return self.tired > 30
        else:
            return self.tired > 80

    def is_hungry(self):
        # We won't eat if we are thirsty.
        if self.is_thirsty():
            return False
        if self.state == "EATING":
            # If already eating, keep on eating.
            return self.hunger > 30
        else:
            return self.hunger > 80

    def is_thirsty(self):
        return self.thirst > 80

    @staticmethod
    def outside_bounds(attribute):
        return attribute < 0 or attribute > 130

    def update(self, changes):
        self.tired += changes[0]
        self.hunger += changes[1]
        self.thirst += changes[2]
        if self.outside_bounds(self.tired) or self.outside_bounds(self.hunger) or self.outside_bounds(self.thirst):
            print("Rogue: " + str(self))
            raise OverflowError

    def new_state(self, state):
        self.state = state.upper()

    def __str__(self):
        return "GuineaPig:(State: {0}, Hunger: {1}, Thirst:{2}, Tired:{3})"\
            .format(self.state, self.hunger, self.thirst, self.tired)


class GuineaPigState:

    def __init__(self, state, changes):
        self.state = state
        self.changes = changes

    def transition(self, gp: GuineaPig):
        pass


class GuineaPigPassive(GuineaPigState):

    def __init__(self, state, changes):
        super(GuineaPigPassive, self).__init__(state, changes)

    def transition(self, gp: GuineaPig):
        gp.update(self.changes)
        if not gp.is_tired():
            new_state = "AWAKE"
        elif random.randint(1, 10) > 8:
            new_state = "STANDBY"
        else:
            new_state = "SLEEPING"
        gp.new_state(new_state)
        return gp


class GuineaPigActive(GuineaPigState):

    def __init__(self, state, changes):
        super(GuineaPigActive, self).__init__(state, changes)

    def transition(self, gp: GuineaPig):
        gp.update(self.changes)
        if gp.is_tired():
            new_state = "SLEEPING"
        elif gp.is_hungry():
            new_state = "EATING"
        elif gp.is_thirsty():
            new_state = "DRINKING"
        elif random.randint(1, 10) > 8:
            new_state = "WANDERING"
        elif random.randint(1, 10) > 1:
            new_state = "STANDBY"
        else:
            new_state = "AWAKE"
        gp.new_state(new_state)
        return gp
