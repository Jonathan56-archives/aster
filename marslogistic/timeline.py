

class TimeLine(object):
    def __init__(self, simulation):
        self.sim = simulation
        self.earth_launch = None

        # Start process to open window
        self.sim.env.process(self.open_window())

    def open_window(self):
        while True:
            # Wait until window open
            yield self.sim.env.timeout(2 * 365 * 24 * 60 * 60)

            # Trigger signal for launchpads
            self.sim.logger.log(
                self, 'Launch window open', key='launch_window_open')
            self.earth_launch = self.sim.env.process(self.sim.earth.launchpad.start())

            # Wait until window closes
            yield self.sim.env.timeout(30 * 24 * 60 * 60)
            self.earth_launch.interrupt()
            self.earth_launch = None  # The process was just closed
