

class TimeLine(object):
    def __init__(self, simulation):
        self.sim = simulation
        self.earth_launch = None

        # Start process to open window
        self.sim.env.process(self.open_window())

        # Start process to close window
        self.sim.env.process(self.close_window())

    def open_window(self):
        while True:
            # Wait until window open
            yield self.sim.env.timeout(2 * 365 * 24 * 60 * 60)

            # Trigger signal for launchpads
            self.earth_launch = self.sim.env.process(self.sim.earth.launchpad.start())
            yield self.earth_launch

    def close_window(self):
        while True:
            # Wait until window close
            yield self.sim.env.timeout(2 * 365 * 24 * 60 * 60 + 30 * 24 * 60 * 60)
            self.earth_launch.interrupt()
