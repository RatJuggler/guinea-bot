from time import sleep


class Age:

    def __init__(self, duration: int, interval: int, accelerated: bool) -> None:
        """
        Initialise an age tracking instance.
        :param duration: How long to track the age in days
        :param interval: The time interval between each tick of the age clock
        :param accelerated: Don't wait for the time interval
        """
        self.__duration = duration
        self.__interval = interval
        self.__accelerated = accelerated
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

    def increase(self) -> bool:
        """
        Increase age and pause if we aren't running in accelerated mode.
        :return: True while age is less than final age, otherwise False
        """
        self.__age_clock += 1
        if not self.__accelerated:
            sleep(self.__interval * 60)
        return self.__age_clock < self.__max_age

    def stats(self, duration: int) -> [float, str]:
        """
        Calculate percentage and average time spent for given duration.
        :param duration: to calculate stats for
        :return: Percentage and average time
        """
        percentage = duration / self.__age_clock * 100
        average = self.__format_age_time(duration * self.__interval // self.__duration)
        return percentage, average

    def __str__(self) -> str:
        """
        Build a string showing the current internal state.
        :return: String representation of the current instance.
        """
        return self.__format_age_day_time()
