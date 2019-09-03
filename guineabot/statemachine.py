

class StateMachine:

    def __init__(self):
        self.states = {}
        self.counts = {}

    def add_state(self, name, handler, changes):
        name = name.upper()
        self.states[name] = handler(name, changes)
        self.counts[name] = 0

    @staticmethod
    def format_time(tick, interval):
        total_minutes = tick * interval
        hours = total_minutes // 60
        minutes = total_minutes - (hours * 60)
        return "{0:02d}:{1:02d}".format(hours, minutes)

    def run(self, condition, days, interval):
        ticks = (24 * 60) // interval
        print("Days: {0}, Interval: {1} mins, Ticks: {2}".format(days, interval, ticks))
        for day in range(days):
            print("Day: {0}".format(day))
            for i in range(ticks):
                new_state = condition.state
                print("{0} >> {1}".format(self.format_time(i, interval), str(condition)))
                state = self.states[new_state]
                self.counts[new_state] += 1
                condition = state.transition(condition)
        for state in self.counts:
            print("{0:9} : {1:04.2f}% - {2}".format(state, self.counts[state] / (ticks * days) * 100,
                                                    self.format_time(self.counts[state] // days, interval)))
