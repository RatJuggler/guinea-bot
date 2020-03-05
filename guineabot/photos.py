import glob
from random import choice
from typing import List

from age_logging import age_logger


class Photos:

    @staticmethod
    def __load_photos(path_to_photos: str) -> List[str]:
        """
        Load a list of the photos available to tweet.
        :param path_to_photos: Path to folder of jpg files
        :return: List of full paths to each photo
        """
        if path_to_photos == "":
            return []
        age_logger.info("Loading photos from: {0}".format(path_to_photos))
        return [f for f in glob.glob(path_to_photos + "/*.jpg", recursive=False)]

    def __init__(self, path_to_photos: str) -> None:
        """
        Initialise the photos list.
        :param path_to_photos: Path to folder of photos for tweeting
        """
        self.__photos = self.__load_photos(path_to_photos)

    def loaded(self) -> bool:
        return len(self.__photos) > 0

    def get_path_to_random(self) -> str:
        return choice(self.__photos)
