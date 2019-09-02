

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

    def run(self, start_state, cargo, days, interval):
        ticks = (24 * 60) // interval
        print("Days: {0}, Interval: {1} mins, Ticks: {2}".format(days, interval, ticks))
        new_state = start_state
        for run in range(days):
            for i in range(ticks):
                new_state = new_state.upper()
                print("{0} >> {1:9} - {2}".format(self.format_time(i, interval), new_state, str(cargo)))
                state = self.states[new_state]
                self.counts[new_state] += 1
                (new_state, cargo) = state.transition(cargo)
            print("Run: {0} - {1}".format(run, str(cargo)))
        for state in self.counts:
            print("{0:9} : {1:04.2f}% - {2}".format(state, self.counts[state] / (ticks * days) * 100,
                                                    self.format_time(self.counts[state] // days, interval)))
