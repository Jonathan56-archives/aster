import factory as f
import storage as s


class Body(object):
    def __init__(self, situation, name):
        self.sim = simulation
        self.name = name

        # Initialize from input database
        self.gravity = self.sim.db[name, 'gravity']


class Earth(Body):
    def __init__(self, simulation):
        self._super(simulation, 'earth')

        # Storages
        self.propelant_stock = s.Propellant(self, name_from_input)

        # Factories
        self.propelant_factory = f.Propellant(self, name_from_input)
        self.booster_factory = …
        self.tanker_factory = …
