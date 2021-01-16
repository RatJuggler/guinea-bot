import json

from typing import List

from .age_logging import age_logger
from .age_tracker import AgeTracker
from .tweeter import Tweeter


class GuineaPig:
    """
    A guinea pig.
    """

    def __init__(self, name: str, age: AgeTracker, start_state: str, tired: int, hunger: int, thirst: int,
                 tweeter: Tweeter) -> None:
        """
        Initialise the guinea pig.
        :param name: Name of the guinea pig bot
        :param age: Age tracker
        :param start_state: Initial state
        :param tired: Initial value of tired attribute
        :param hunger: Initial value of hunger attribute
        :param thirst: Initial value of thirst attribute
        :param tweeter: To generate tweets with
        """
        self.__name = name
        self.__age = age
        self.__state = start_state.upper()
        self.__tired = tired
        self.__hunger = hunger
        self.__thirst = thirst
        self.__tweeter = tweeter

    def age(self) -> AgeTracker:
        return self.__age

    def is_tired(self) -> bool:
        """
        Decide if the guinea pig is tired.
        We won't sleep if we are hungry or thirsty.
        :return: True if tired, otherwise False
        """
        if self.is_hungry() or self.is_thirsty():
            return False
        if self.__state == "SLEEPING":
            # If we are already sleeping, carry on sleeping.
            return self.__tired > 30
        else:
            return self.__tired > 80

    def is_hungry(self) -> bool:
        """
        Decide if the guinea pig is hungry.
        We won't eat if we are thirsty.
        :return: True if hungry, otherwise False
        """
        if self.is_thirsty():
            return False
        if self.__state == "EATING":
            # If already eating, keep on eating.
            return self.__hunger > 30
        else:
            return self.__hunger > 80

    def is_thirsty(self) -> bool:
        """
        Decide if the guinea pig is thirsty.
        :return: True if thirsty, otherwise False
        """
        return self.__thirst > 80

    @staticmethod
    def __outside_bounds(attribute) -> bool:
        """
        Reasonable check for guinea pig attribute.
        :param attribute: To check
        :return: True if outside expected range, otherwise False
        """
        return attribute < 0 or attribute > 130

    def __rogue_pig(self) -> bool:
        """
        Check if any attributes have gone outside of a reasonable range.
        :return: True anything outside of reasonable range, otherwise False
        """
        return self.__outside_bounds(self.__tired) or \
            self.__outside_bounds(self.__hunger) or \
            self.__outside_bounds(self.__thirst)

    def update(self, new_state: str, changes: List[int]) -> bool:
        """
        Update attributes driven by the change of state, check chance to tweet and then increase the age.
        :param new_state: The new state to move to
        :param changes: To apply to the attributes
        :return: True while the guinea pig hasn't reached it's age limit, otherwise False
        """
        age_logger.set_age(self.__age)
        self.__tired += changes[0]
        self.__hunger += changes[1]
        self.__thirst += changes[2]
        if self.__rogue_pig():
            age_logger.error("Rogue Pig: {0}".format(str(self)))
            raise OverflowError
        if self.__state != new_state:
            self.__state = new_state
            self.__tweeter.tweet_state(self.__state)
        return self.__age.increase()

    def repr_json(self) -> str:
        """
        Build a string to represent the object in JSON.
        :return: JSON string of key object attributes.
        """
        state = dict(__class__=self.__class__.__name__,
                     __module__=self.__module__,
                     name=self.__name,
                     age=self.__age.repr_json(),
                     state=self.__state,
                     tired=self.__tired,
                     hunger=self.__hunger,
                     thirst=self.__thirst)
        return json.dumps(state)

    def __str__(self) -> str:
        """
        Build a string showing the current internal state.
        :return: String representation of the current instance.
        """
        return "GuineaPig:(Name: {0}, State: {1}, Hunger: {2}, Thirst: {3}, Tired: {4})"\
            .format(self.__name, self.__state, self.__hunger, self.__thirst, self.__tired)


def create_guinea_pig(name: str, duration: int, interval: int, accelerated: bool, tweeter: Tweeter) -> GuineaPig:
    """
    Create a new guinea pig instance.
    :param name: Of the guinea pig
    :param duration: How long the guinea pig will live
    :param interval: The time interval between each tick of the age clock
    :param accelerated: Don't wait for the time interval
    :param tweeter: To generate tweet with
    :return: A new instance of a guinea pig
    """
    age = AgeTracker(duration, interval, accelerated)
    return GuineaPig(name, age, "SLEEPING", 20, 10, 10, tweeter)
