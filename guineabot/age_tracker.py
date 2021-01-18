

class AgeTracker:
    """
    Acts like a virtual clock tracking over a duration.
    """

    def __init__(self, duration: int, interval: int) -> None:
        """
        Initialise an age tracking instance.
        :param duration: How long to track the age in days
        :param interval: The time interval between each tick of the age clock
        """
        self.__duration = duration
        self.__interval = interval
        # Calculate the number of interval ticks over the duration.
        self.__max_age = (self.__duration * 24 * 60) // self.__interval
        self.__age_clock = 0

    @staticmethod
    def __format_age_time(minutes: int) -> str:
        """
        Format minutes of age time.
        :param minutes: to format
        :return: String of minutes in HH:MM format
        """
        hours = minutes // 60
        minutes -= hours * 60
        return "{0:02d}:{1:02d}".format(hours, minutes)

    def __format_age_day_time(self) -> str:
        """
        Format the age into days, hours and minutes.
        :return: Age in DAY - HH:MM format
        """
        minutes = self.__age_clock * self.__interval
        days = minutes // (24 * 60)
        minutes -= days * 24 * 60
        return "Age: {0:d} - {1}".format(days, self.__format_age_time(minutes))

    def has_died(self) -> bool:
        """
        Has the bot reached the end of its lifespan?
        :return: True once age reaches final age, otherwise False
        """
        return self.__age_clock >= self.__max_age

    def increase(self) -> None:
        """
        Increase age and pause if we aren't running in accelerated mode.
        :return: No meaningful return
        """
        self.__age_clock += 1

    def repr_dict(self) -> dict:
        """
        Build a dictionary to represent the object.
        :return: Dictionary of key object attributes.
        """
        return dict(__class__=self.__class__.__name__,
                    __module__=self.__module__,
                    duration=self.__duration)

    def __str__(self) -> str:
        """
        Build a string showing the current internal state.
        :return: String representation of the current instance.
        """
        return self.__format_age_day_time()
