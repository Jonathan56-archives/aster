import pandas


class Simulation(object):
    def __init__(self, db, events):
        # Input parameters
        self.db = db
        self.events = events

        # Simulation parameters
        self.env = simply.Env()
        self.bodies = []

        # Ouputs
        # {'level', 'datetime', 'object_type',
        # 'object_id', 'object', 'message'}
        self.log = []

    def initialize(self):
        pass

    def run(self, until):
        pass
