import json
import glob
import pathlib

from random import choice, randint
from typing import List, Dict

from .smt_logging import smt_logger
from .statemachine import StateMachine, State
from .twitter_api import TwitterService


# Current guinea pig states.
SLEEPING = "SLEEPING"
EATING = "EATING"
DRINKING = "DRINKING"
WANDERING = "WANDERING"
THINKING = "THINKING"
AWAKE = "AWAKE"
# Sayings for photo tweets.
PHOTOS = "PHOTOS"


class GuineaPig:

    @staticmethod
    def __load_sayings() -> Dict[str, List[str]]:
        sayings_file = pathlib.Path(__file__).parent / "guinea_pig_sayings.json"
        smt_logger.info("Loading sayings from: {0}".format(sayings_file))
        with sayings_file.open('r', encoding='utf-8') as f:
            sayings_loaded = json.load(f)
        state_sayings = {}
        for state in sayings_loaded['states']:
            state_sayings[state['state']] = state['sayings']
        return state_sayings

    @staticmethod
    def __load_photos(path_to_photos: str) -> List[str]:
        if path_to_photos == "":
            return []
        smt_logger.info("Loading photos from: {0}".format(path_to_photos))
        return [f for f in glob.glob(path_to_photos + "/*.jpg", recursive=False)]

    def __init__(self, name: str, start_state: str, tired: int, hunger: int, thirst: int,
                 path_to_photos: str, twitter_service: TwitterService) -> None:
        self.__name = name
        self.__state = start_state.upper()
        self.__tired = tired
        self.__hunger = hunger
        self.__thirst = thirst
        self.__sayings = self.__load_sayings()
        self.__photos = self.__load_photos(path_to_photos)
        self.__twitter_service = twitter_service
        self.__friends = self.__twitter_service.get_current_friends()

    def is_tired(self) -> bool:
        # We won't sleep if we are hungry or thirsty.
        if self.is_hungry() or self.is_thirsty():
            return False
        if self.__state == SLEEPING:
            # If we are already sleeping, carry on sleeping.
            return self.__tired > 30
        else:
            return self.__tired > 80

    def is_hungry(self) -> bool:
        # We won't eat if we are thirsty.
        if self.is_thirsty():
            return False
        if self.__state == EATING:
            # If already eating, keep on eating.
            return self.__hunger > 30
        else:
            return self.__hunger > 80

    def is_thirsty(self) -> bool:
        return self.__thirst > 80

    @staticmethod
    def outside_bounds(attribute) -> bool:
        return attribute < 0 or attribute > 130

    def __get_saying_for_state(self, state_to_find: str) -> str:
        return choice(self.__sayings[state_to_find])

    def __tweet_state(self, new_state: str) -> None:
        if self.__state != new_state:
            self.__state = new_state
            if randint(1, 5) == 1:
                self.__twitter_service.tweet(self.__get_saying_for_state(self.__state))
        elif randint(1, 60) == 1:
            if len(self.__photos) > 0:
                self.__twitter_service.tweet_with_photo(self.__get_saying_for_state(PHOTOS), choice(self.__photos))
        elif randint(1, 60) == 1:
            self.__friends = self.__twitter_service.find_new_friend(self.__friends)

    def update(self, new_state: str, changes: List[int]) -> None:
        self.__tired += changes[0]
        self.__hunger += changes[1]
        self.__thirst += changes[2]
        if self.outside_bounds(self.__tired) or self.outside_bounds(self.__hunger) or self.outside_bounds(self.__thirst):
            smt_logger.error("Rogue Pig: {0}".format(str(self)))
            raise OverflowError
        self.__tweet_state(new_state)

    def __str__(self):
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
