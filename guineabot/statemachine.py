from time import sleep


class StateMachine:

    def __init__(self, interval, days):
        self.interval = interval
        self.days = days
        self.run_time = (self.days * 24 * 60) // self.interval
        self.states = {}
        self.counts = {}

    def add_state(self, name, handler, changes):
        name = name.upper()
        self.states[name] = handler(name, changes)
        self.counts[name] = 0

    def format_time(self, ticks):
        total_minutes = ticks * self.interval
        days = total_minutes // (24 * 60)
        total_minutes -= days * 24 * 60
        hours = total_minutes // 60
        minutes = total_minutes - (hours * 60)
        return "{0:02d} {1:02d}:{2:02d}".format(days, hours, minutes)

    def run(self, data):
        for i in range(self.run_time):
            new_state = data.state
            print("{0} >> {1}".format(self.format_time(i), str(data)))
            state = self.states[new_state]
            self.counts[new_state] += 1
            data = state.transition(data)
            sleep(self.interval * 60)

    def stats(self):
        for state in self.counts:
            print("{0:9} : {1:04.2f}% - {2}".format(state, self.counts[state] / self.run_time * 100,
                                                    self.format_time(self.counts[state] // self.days)))
