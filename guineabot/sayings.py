import json
import pathlib

from random import choice
from typing import Dict, List

from .age_logging import age_logger


class Sayings:

    @staticmethod
    def __load_sayings(sayings_file: pathlib.Path) -> Dict[str, List[str]]:
        """
        Load sayings from JSON file, see: guinea-pig-sayings-scheme.json
        :return: Dict of sayings for each state
        """
        age_logger.info("Loading sayings from: {0}".format(sayings_file))
        with sayings_file.open('r', encoding='utf-8') as f:
            sayings_loaded = json.load(f)
        state_sayings = {}
        for state in sayings_loaded['states']:
            state_sayings[state['state']] = state['sayings']
        return state_sayings

    def __init__(self, sayings_file: str = str(pathlib.Path(__file__).parent / "guinea_pig_sayings.json")) -> None:
        """
        Initialise the sayings.
        :param sayings_file: Path to file of sayings
        """
        sayings_file = pathlib.Path(sayings_file)
        if not sayings_file.exists():
            raise FileNotFoundError
        self.__sayings = self.__load_sayings(sayings_file)

    def get_random_saying(self, state: str) -> str:
        """
        Choose a saying to tweet.
        :param state: To find sayings for
        :return: Saying to tweet
        """
        return choice(self.__sayings[state])

    def get_random_photo_saying(self) -> str:
        """
        Choose a saying to go with a photo tweet.
        :return: Saying to tweet
        """
        return self.get_random_saying("PHOTOS")
