from random import randint
from typing import List

from .photos import Photos
from .sayings import Sayings
from .smt_logging import smt_logger
from .statemachine import StateMachine, State
from .twitter_api import TwitterService, get_twitter_service

# Current guinea pig states.
SLEEPING = "SLEEPING"
EATING = "EATING"
DRINKING = "DRINKING"
WANDERING = "WANDERING"
THINKING = "THINKING"
AWAKE = "AWAKE"
# Special state for sayings for photo tweets.
PHOTOS = "PHOTOS"


class GuineaPig:
    """
    A guinea pig.
    """

    def __init__(self, name: str, start_state: str, tired: int, hunger: int, thirst: int,
                 sayings: Sayings, photos: Photos, twitter_service: TwitterService) -> None:
        """
        Initialise the guinea pig state.
        :param name: Name of the guinea pig bot
        :param start_state: Initial state
        :param tired: Initial value of tired attribute
        :param hunger: Initial value of hunger attribute
        :param thirst: Initial value of thirst attribute
        :param sayings: Supplies sayings for tweeting
        :param photos: Supplies photos for tweeting
        :param twitter_service: Twitter service to use
        """
        self.__name = name
        self.__state = start_state.upper()
        self.__tired = tired
        self.__hunger = hunger
        self.__thirst = thirst
        self.__sayings = sayings
        self.__photos = photos
        self.__twitter_service = twitter_service
        self.__friends = self.__twitter_service.get_current_friends()

    def is_tired(self) -> bool:
        """
        Decide if the guinea pig is tired.
        We won't sleep if we are hungry or thirsty.
        :return: True if tired, otherwise False
        """
        if self.is_hungry() or self.is_thirsty():
            return False
        if self.__state == SLEEPING:
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
        if self.__state == EATING:
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
    def outside_bounds(attribute) -> bool:
        """
        Reasonable check for guinea pig attributes.
        :param attribute: To check
        :return: True if outside expected range, otherwise False
        """
        return attribute < 0 or attribute > 130

    def __tweet_state(self, new_state: str) -> None:
        """
        Tweet, tweet with photo, find new friends or prune existing friends.
        This is limited using random checks to prevent the timeline being flooded and from accumulating friends too quickly.
        :param new_state: drives tweet selection
        :return: No meaningful return
        """
        if self.__state != new_state:
            self.__state = new_state
            if randint(1, 5) == 1:
                self.__twitter_service.tweet(self.__sayings.get_random_saying(self.__state))
        elif randint(1, 60) == 1:
            if self.__photos.loaded():
                self.__twitter_service.tweet_with_photo(self.__sayings.get_random_saying(PHOTOS),
                                                        self.__photos.get_path_to_random())
        elif randint(1, 60) == 1:
            self.__friends = self.__twitter_service.find_new_friend(self.__friends)
        elif randint(1, 200) == 1:
            self.__friends = self.__twitter_service.prune_friends(self.__friends)

    def update(self, new_state: str, changes: List[int]) -> None:
        """
        Update attributes driven by change of state.
        :param new_state:
        :param changes:
        :return: No meaningful return
        """
        self.__tired += changes[0]
        self.__hunger += changes[1]
        self.__thirst += changes[2]
        if self.outside_bounds(self.__tired) or self.outside_bounds(self.__hunger) or self.outside_bounds(self.__thirst):
            smt_logger.error("Rogue Pig: {0}".format(str(self)))
            raise OverflowError
        self.__tweet_state(new_state)

    def __str__(self) -> str:
        """
        Build a string showing the current internal state.
        :return: String representation of the current instance.
        """
        return "GuineaPig:(Name: {0}, State: {1}, Hunger: {2}, Thirst: {3}, Tired: {4})"\
            .format(self.__name, self.__state, self.__hunger, self.__thirst, self.__tired)


class GuineaPigState(State):
    """
    The common class which defines each state of the guinea pig.
    """

    def __init__(self, state_name: str, changes: List[int]) -> None:
        """
        Initialise a guinea pig state instance.
        :param state_name: The name of the state
        :param changes: The guinea pig attributes the state affects
        """
        self.__changes = changes
        super(GuineaPigState, self).__init__(state_name.upper())

    def transition(self, gp: GuineaPig) -> str:
        """
        Determine the next state for the given guinea pig.
        :param gp: A guinea pig instance
        :return: The name of the next state (not necessarily different to the current state)
        """
        gp.update(self.get_name(), self.__changes)
        if gp.is_tired():
            new_state = SLEEPING
        elif gp.is_hungry():
            new_state = EATING
        elif gp.is_thirsty():
            new_state = DRINKING
        elif randint(1, 10) > 5:
            new_state = WANDERING
        elif randint(1, 10) > 8:
            new_state = THINKING
        else:
            new_state = AWAKE
        return new_state


def add_guinea_pig_states(sm: StateMachine) -> None:
    """
    Populate a state machine with a guinea pig simulation.
    :param sm: A state machine instance
    :return: No meaningful return.
    """
    sm.add_state(GuineaPigState(SLEEPING, [-20, 3, 1]))
    sm.add_state(GuineaPigState(AWAKE, [5, 5, 2]))
    sm.add_state(GuineaPigState(THINKING, [1, 3, 1]))
    sm.add_state(GuineaPigState(EATING, [5, -10, 4]))
    sm.add_state(GuineaPigState(DRINKING, [5, 5, -80]))
    sm.add_state(GuineaPigState(WANDERING, [10, 10, 5]))


def create_guinea_pig(name: str, path_to_photos: str, quiet: bool) -> GuineaPig:
    """
    Create a new guinea pig instance.
    :param name: Of the guinea pig
    :param path_to_photos: Path to folder of photos for tweeting
    :param quiet: Run without invoking the Twitter API
    :return: A new instance of a guinea pig
    """
    return GuineaPig(name, SLEEPING, 20, 10, 10, Sayings(), Photos(path_to_photos), get_twitter_service(quiet))
