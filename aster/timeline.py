import util
import pandas


class TimeLine(object):
    def __init__(self, simulation):
        self.sim = simulation
        self.earth_launch = None
        self.mars_launch = None

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
            self.mars_launch = self.sim.env.process(self.sim.mars.launchpad.start())

            # Wait until window closes
            yield self.sim.env.timeout(30 * 24 * 60 * 60)
            self.earth_launch.interrupt()
            self.mars_launch.interrupt()
            self.earth_launch = None  # The process was just closed
            self.mars_launch = None

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


class TimeLineFactory(object):
    def __init__(self, filename, existing_timeline=False):
        self.filename = filename
        if not existing_timeline:
            self.timeline = pandas.DataFrame()
        else:
            self.timeline = pandas.read_excel(existing_timeline)
        self._cache = {}

    def interpolate_timeserie(self, dates, values, new_freq):
        """Interpolate a time serie from a few data points"""
        # Create a date range
        date_range = pandas.date_range(start=dates[0], end=dates[-1], freq=new_freq)
        timeserie = pandas.DataFrame(index=date_range, columns=['value'])

        # Set existing values
        for date, value in zip(dates, values):
            #TODO replace with the closest date, instead of the exact date?
            timeserie.loc[date, 'value'] = value

        # Interpolate
        timeserie['value'] = pandas.to_numeric(timeserie['value'])
        timeserie['value'] = timeserie['value'].interpolate(method='time')

        # Format frame
        timeserie['datetime'] = date_range
        timeserie['index'] = range(0, len(date_range))
        timeserie.set_index('index', inplace=True)
        return timeserie

    def add_to_timeline(self, timeserie, colony='None', event='None',
                        structure='None', parameter='None', unit='None'):
        """Add a timeserie to the timeline"""
        # Create a dataframe from inputs
        frame = timeserie.copy()
        frame['colony'] = [colony] * len(frame)
        frame['event'] = [event] * len(frame)
        frame['parameter'] = [parameter] * len(frame)
        frame['structure'] = [structure] * len(frame)
        frame['unit'] = [unit] * len(frame)

        # Concat frames
        self._cache[colony + event +
                    parameter + structure + unit] = frame

    def save(self):
        # Concat the timeline together
        for key in self._cache:
            self.timeline = pandas.concat([self.timeline, self._cache[key]], axis=0)

        # Order by time the table
        self.timeline = self.timeline.sort_values(by='datetime')
        self.timeline.reset_index(inplace=True, drop=True)

        # Save to excel
        writer = pandas.ExcelWriter(self.filename)
        self.timeline.to_excel(writer)
        writer.save()
