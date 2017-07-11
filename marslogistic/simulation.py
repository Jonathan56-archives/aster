from __future__ import division
import pandas as pd
import datetime as dt
import colony as col
import timeline as t
import simpy

class Simulation(object):
    def __init__(self, db, initial, timeline):
        # Input parameters
        self.db = db
        self.initial = initial
        self.input_timeline = timeline

        # Simulation parameters
        self.env = simpy.Environment()
        self.start = dt.datetime(2020, 1, 1, 0, 0, 0)
        self.end = dt.datetime(2030, 1, 1, 0, 0, 0)
        self.earth = None
        self.timeline = None

        # Ouputs
        # {'level', 'datetime', 'object_type',
        # 'object_id', 'object', 'message'}
        self.log = None

    def initialize(self):
        # Set the log to an empty list
        self.log = []

    def run(self):
        """Create bodies and start the simulation"""
        # Reset the simulation
        self.initialize()

        # Create earth
        self.earth = col.Earth(self)

        # # Change parameters with time
        # self.timeline = t.TimeLine(self)

        # Launch the simulation
        self.env.run(until=(self.end - self.start).total_seconds())

    def post_run(self):
        """Post processes"""
        # Format the logs
        self.log = pd.DataFrame(self.log)

        # Pause the simulation before it quits
        import pudb; pudb.set_trace()

    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        return setattr(self, name, value)

    def __delitem__(self, name):
        return delattr(self, name)

    def __contains__(self, name):
        return hasattr(self, name)
