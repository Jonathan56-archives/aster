from __future__ import division
import pandas as pd
import datetime as dt
import colony as col
import timeline as t
import monitoring as m
import simpy
import progressbar
import util
import os


class Simulation(object):
    def __init__(self, db, timeline):
        # Input parameters
        self.db = db
        self.timeline = timeline
        self.initial = None
        self.cwd = os.getcwd()

        # Simulation parameters
        self.env = simpy.Environment()
        self.start = timeline.datetime.iloc[0]
        self.end = timeline.datetime.iloc[-1]
        self.earth = None
        self.mars = None

        # Ouputs
        self.logger = None
        self.log = None
        self.monitor = None

    def initialize(self):
        # Set the log to an empty list
        self.logger = m.Logger(self)
        self.log = []

        # Create the initial parameters
        self.initial = self.timeline[self.timeline.event == 'initial'].copy()

        # Create progress bar
        self.progressbar = progressbar.ProgressBar(widgets=['Simulation: ',
                                           progressbar.Percentage(),
                                           progressbar.Bar()],
                                           maxval=util.now_to_date_in_seconds(
                                            self, self.end)).start()

    def run(self):
        """Create bodies and start the simulation"""
        # Reset the simulation
        self.initialize()

        # Create earth
        self.earth = col.Earth(self)
        self.earth_LEO = col.Earth_LEO(self)
        self.mars = col.Mars(self)

        # # Change parameters with time
        self.tline = t.TimeLine(self)

        # Launch the simulation
        self.env.process(util.update_progressbar(self))
        self.env.run(until=(self.end - self.start).total_seconds())
        self.progressbar.finish()

        # Post processes
        self.post_run()

    def post_run(self):
        """Post processes"""
        # Format the logs
        self.log = pd.DataFrame(self.log)

        # Write logs to result folder
        result_folder = os.path.join(self.cwd, 'results')
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)
        self.log.to_csv(os.path.join(result_folder, 'logs.csv'))
        # util.plot_results(result_folder, 'logs.csv')

    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        return setattr(self, name, value)

    def __delitem__(self, name):
        return delattr(self, name)

    def __contains__(self, name):
        return hasattr(self, name)
