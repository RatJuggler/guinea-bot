

class AgeTracker:
    """
    Acts like a virtual clock tracking over a duration.
    """

    def __init__(self, interval: int) -> None:
        """
        Initialise an age tracking instance.
        :param interval: The time interval between each tick of the age clock
        """
        self.__interval = interval
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

    def increase(self) -> None:
        """
        Increase age and pause if we aren't running in accelerated mode.
        :return: No meaningful return
        """
        self.__age_clock += 1

    def __str__(self) -> str:
        """
        Build a string showing the current internal state.
        :return: String representation of the current instance.
        """
        return self.__format_age_day_time()
