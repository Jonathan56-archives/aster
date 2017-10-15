import util

class TimeLine(object):
    def __init__(self, simulation):
        self.sim = simulation
        self.earth_launch = None

        # Start process to open window
        self.sim.env.process(self.open_window())

        # Start process of updating factories
        self.sim.env.process(self.timeline_update())

    def open_window(self):
        # Select "window_open" rows
        timeline_open = self.sim.timeline[self.sim.timeline.event == 'window_open']

        # Loop over all the window_open
        for index, row in timeline_open.iterrows():
            # Wait until window open (every 26 months)
            yield self.sim.env.timeout(
                util.now_to_date_in_seconds(self.sim, row.datetime))

            # Trigger signal for launchpads
            self.sim.logger.log(
                self, 'Launch window open', key='launch_window_open')
            self.earth_launch = self.sim.env.process(self.sim.earth.launchpad.start())

            # Wait until window closes
            yield self.sim.env.timeout(30 * 24 * 60 * 60)
            self.earth_launch.interrupt()
            self.earth_launch = None  # The process was just closed

    def timeline_update(self):
        # Select "update" rows
        timeline_updates = self.sim.timeline[self.sim.timeline.event == 'update']

        # Loop over all the updates
        for index, row in timeline_updates.iterrows():

            # Wait until it's time to apply the update
            yield self.sim.env.timeout(
                util.now_to_date_in_seconds(self.sim, row.datetime))

            # Update parameter
            self.sim[row.colony][row.structure][row.parameter] = row.value
