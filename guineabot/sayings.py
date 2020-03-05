import json
import pathlib
from random import choice
from typing import Dict, List

from .smt_logging import smt_logger


class Sayings:

    @staticmethod
    def __load_sayings() -> Dict[str, List[str]]:
        """
        Load sayings from JSON file, see: guinea-pig-sayings-scheme.json
        :return: Dict of sayings for each state
        """
        sayings_file = pathlib.Path(__file__).parent / "guinea_pig_sayings.json"
        smt_logger.info("Loading sayings from: {0}".format(sayings_file))
        with sayings_file.open('r', encoding='utf-8') as f:
            sayings_loaded = json.load(f)
        state_sayings = {}
        for state in sayings_loaded['states']:
            state_sayings[state['state']] = state['sayings']
        return state_sayings

    def __init__(self) -> None:
        """
        Initialise the sayings.
        """
        self.__sayings = self.__load_sayings()

    def get_saying_for_state(self, state: str) -> str:
        """
        Choose a saying to tweet.
        :param state: To find sayings for
        :return: Saying to tweet
        """
        return choice(self.__sayings[state])
