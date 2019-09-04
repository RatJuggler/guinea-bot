import json
import pathlib
import random

from .twitter_api import tweet


class GuineaPig:

    @staticmethod
    def __load_sayings():
        sayings_file = pathlib.Path(__file__).parent / "guinea_pig_sayings.json"
        with sayings_file.open('r') as f:
            sayings = json.load(f)
        return sayings["states"]

    def __init__(self, start_state, tired, hunger, thirst):
        self.state = start_state.upper()
        self.tired = tired
        self.hunger = hunger
        self.thirst = thirst
        self.sayings = self.__load_sayings()

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

    def update_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            for state in self.sayings:
                if state["state"] == self.state:
                    tweet(random.choice(state["sayings"]))

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
            new_state = "THINKING"
        else:
            new_state = "SLEEPING"
        gp.update_state(new_state)
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
            new_state = "THINKING"
        else:
            new_state = "AWAKE"
        gp.update_state(new_state)
        return gp
