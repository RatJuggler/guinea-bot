import json

from pathlib import Path
from typing import List

from .age_logging import age_logger
from .tweeter import Tweeter


def format_filename(name: str) -> str:
    return str(Path.home()) + '/' + name + ".json"


class GuineaPig:
    """
    A guinea pig.
    """

    def __init__(self, name: str, lifespan: int, current_age: int, start_state: str, tired: int, hunger: int, thirst: int,
                 tweeter: Tweeter) -> None:
        """
        Initialise the guinea pig.
        :param name: Name of the guinea pig bot
        :param lifespan: Of the guinea pig in days
        :param current_age: Of the guinea pig in minutes
        :param start_state: Initial state
        :param tired: Initial value of tired attribute
        :param hunger: Initial value of hunger attribute
        :param thirst: Initial value of thirst attribute
        :param tweeter: To generate tweets with
        """
        self.__name = name
        self.__lifespan = lifespan
        self.__max_age = self.__lifespan * 24 * 60
        self.__current_age = current_age
        self.__state = start_state.upper()
        self.__tired = tired
        self.__hunger = hunger
        self.__thirst = thirst
        self.__tweeter = tweeter

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

    def has_died(self) -> bool:
        """
        Decide if the guinea has died.
        :return: True once the guinea pig reaches it's age limit, otherwise False
        """
        return self.__current_age >= self.__max_age

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

    def save_state(self) -> None:
        """
        Save the guinea pig state.
        :return: No meaningful return
        """
        with open(format_filename(self.__name), 'w') as file:
            json.dump(self.repr_dict(), file, indent=4)

    def update(self, new_state: str, changes: List[int], duration: int) -> None:
        """
        Update attributes driven by the change of state, check chance to tweet and then increase the age.
        :param new_state: The new state to move to
        :param changes: To apply to the attributes
        :param duration: How long the new state will last
        :return: No meaningful return
        """
        age_logger.set_age(self.__current_age)
        self.__tired += changes[0]
        self.__hunger += changes[1]
        self.__thirst += changes[2]
        if self.__rogue_pig():
            age_logger.error("Rogue Pig: {0}".format(str(self)))
            raise OverflowError
        if self.__state != new_state:
            self.__state = new_state
            self.__tweeter.tweet_state(self.__state)
        self.__current_age += duration
        age_logger.debug(self.__str__())
        self.save_state()

    def rejuvenate(self) -> None:
        """
        Bring the guinea pig back to life.
        :return: No meaningful return
        """
        self.__state = "SLEEPING"
        self.__current_age = 0

    def repr_dict(self) -> dict:
        """
        Build a dictionary to represent the object.
        :return: Dictionary of key object attributes.
        """
        return dict(__class__=self.__class__.__name__,
                    __module__=self.__module__,
                    name=self.__name,
                    lifespan=self.__lifespan,
                    current_age=self.__current_age,
                    state=self.__state,
                    tired=self.__tired,
                    hunger=self.__hunger,
                    thirst=self.__thirst)

    def __str__(self) -> str:
        """
        Build a string showing the current internal state.
        :return: String representation of the current instance.
        """
        return "GuineaPig:(Name: {0}, Lifespan: {1} days, Current Age: {2} mins, State: {3}, Tired: {4}, Hunger: {5}, Thirst: {6})"\
            .format(self.__name, self.__lifespan, self.__current_age, self.__state, self.__tired, self.__hunger, self.__thirst)


def create_guinea_pig(name: str, lifespan: int, tweeter: Tweeter) -> GuineaPig:
    """
    Create a new guinea pig instance or load from a previous save.
    :param name: Of the guinea pig
    :param lifespan: How long the guinea pig will live
    :param tweeter: To generate tweet with
    :return: A new instance of a guinea pig
    """
    save_file = format_filename(name)
    try:
        with open(save_file, 'r') as reader:
            gp_data = json.load(reader)
            age_logger.info("Previous instance of guinea pig found at '{0}', reanimating!".format(save_file))
            gp = GuineaPig(gp_data["name"],
                           gp_data["lifespan"],
                           gp_data["current_age"],
                           gp_data["state"],
                           gp_data["tired"],
                           gp_data["hunger"],
                           gp_data["thirst"],
                           tweeter)
            if gp.has_died():
                age_logger.info("This is an ex guinea pig, rejuvenating!")
                gp.rejuvenate()
    except FileNotFoundError:
        age_logger.info("No previous instance of guinea pig found, creating a new instance at '{0}'!".format(save_file))
        gp = GuineaPig(name, lifespan, 0, "SLEEPING", 20, 10, 10, tweeter)
        gp.save_state()
    return gp
