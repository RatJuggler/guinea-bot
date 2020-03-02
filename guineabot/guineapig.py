import json
import glob
import logging
import pathlib

from random import choice, randint
from typing import List, Dict

from statemachine import State
from twitter_api import TwitterService


class GuineaPig:

    @staticmethod
    def __load_sayings() -> List[Dict[str, List[str]]]:
        sayings_file = pathlib.Path(__file__).parent / "guinea_pig_sayings.json"
        with sayings_file.open('r', encoding='utf-8') as f:
            sayings = json.load(f)
        return sayings["states"]

    @staticmethod
    def __load_photos(path_to_photos: str) -> List[str]:
        return [f for f in glob.glob(path_to_photos + "/*.jpg", recursive=False)]

    def __init__(self, start_state: str, tired: int, hunger: int, thirst: int,
                 path_to_photos: str, twitter_service: TwitterService) -> None:
        self.state = start_state.upper()
        self.tired = tired
        self.hunger = hunger
        self.thirst = thirst
        self.sayings = self.__load_sayings()
        self.photos = self.__load_photos(path_to_photos)
        self.twitter_service = twitter_service
        self.friends = self.twitter_service.get_current_friends()

    def is_tired(self) -> bool:
        # We won't sleep if we are hungry or thirsty.
        if self.is_hungry() or self.is_thirsty():
            return False
        if self.state == "SLEEPING":
            # If we are already sleeping, carry on sleeping.
            return self.tired > 30
        else:
            return self.tired > 80

    def is_hungry(self) -> bool:
        # We won't eat if we are thirsty.
        if self.is_thirsty():
            return False
        if self.state == "EATING":
            # If already eating, keep on eating.
            return self.hunger > 30
        else:
            return self.hunger > 80

    def is_thirsty(self) -> bool:
        return self.thirst > 80

    @staticmethod
    def outside_bounds(attribute) -> bool:
        return attribute < 0 or attribute > 130

    def __get_saying_for_state(self, state_to_find: str) -> str:
        for state in self.sayings:
            if state["state"] == state_to_find:
                return choice(state["sayings"])

    def __tweet_state(self) -> None:
        # Limit when we tweet and find friends.
        if randint(1, 5) == 1:
            self.twitter_service.tweet(self.__get_saying_for_state(self.state))
        elif randint(1, 40) == 1:
            self.twitter_service.tweet_with_photo(self.__get_saying_for_state("PHOTOS"), choice(self.photos))
        elif randint(1, 50) == 1:
            self.twitter_service.find_new_friend(self.friends)

    def update(self, new_state: str, changes: List[int]) -> None:
        self.tired += changes[0]
        self.hunger += changes[1]
        self.thirst += changes[2]
        if self.outside_bounds(self.tired) or self.outside_bounds(self.hunger) or self.outside_bounds(self.thirst):
            logging.error("Rogue Pig: {0}".format(str(self)))
            raise OverflowError
        if self.state != new_state:
            self.state = new_state
            self.__tweet_state()

    def __str__(self):
        return "GuineaPig:(State: {0}, Hunger: {1}, Thirst:{2}, Tired:{3})"\
            .format(self.state, self.hunger, self.thirst, self.tired)


class GuineaPigState(State):

    def __init__(self, state: str, changes: List[int]):
        self.state = state
        self.changes = changes

    def transition(self, gp: GuineaPig) -> str:
        gp.update(self.state, self.changes)
        if gp.is_tired():
            new_state = "SLEEPING"
        elif gp.is_hungry():
            new_state = "EATING"
        elif gp.is_thirsty():
            new_state = "DRINKING"
        elif randint(1, 10) > 5:
            new_state = "WANDERING"
        elif randint(1, 10) > 8:
            new_state = "THINKING"
        else:
            new_state = "AWAKE"
        return new_state
