import factory as f
import container as c
import storage as s


class Body(object):
    def __init__(self, simulation, name):
        self.sim = simulation
        self.name = name

        # # Initialize from input database
        # self.gravity = self.sim.db[name]['gravity']


class Earth(Body):
    def __init__(self, simulation):
        super(Body, self).__init__(simulation, 'earth')

        # Containers
        self.propelant_container = c.Propellant(self, 'propellant_container')

        # Storages
        self.booster_storage = s.Booster(self, 'booster_storage')
        self.tank_storage = s.Tank(self, 'tank_storage')
        self.orbital_tank_storage = s.OrbitalTank(self, 'orbital_tank_storage')
        self.heartofgold_storage = s.Heartofgold(self, 'heartofgold_storage')

        ## Processes
        # Production
        self.propelant_factory = f.Propellant(self, '')
        self.booster_factory = ...
        self.tanker_factory = ...

        # Launches
        self.heartofgold_launch = ...
        self.tank_launch = ...
