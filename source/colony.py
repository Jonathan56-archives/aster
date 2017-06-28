import factory as f
import storage as s
import launchpad as l
import simpy

class Colony(object):
    def __init__(self, simulation, name):
        self.sim = simulation
        self.name = name


class Earth(Colony):
    def __init__(self, simulation):
        """Create Earth | Add ressources and processes within env"""
        super(Colony, self).__init__(simulation, 'earth')

        ## Containers
        self.propelant_container = simpy.Container(
            self.sim.env, init=100, capacity=1000)

        ## Storages
        self.booster_storage = s.Booster(self, 'booster_storage')
        self.tank_storage = s.Tank(self, 'tank_storage')
        self.heartofgold_storage = s.Heartofgold(self, 'heartofgold_storage')

        ## Processes
        # Factories
        self.propelant_factory = f.Propellant(self, 'propelant_factory')
        self.booster_factory = f.Booster(self, 'booster_factory')
        self.tank_factory = f.Tank(self, 'tank_factory')
        self.heartofgold_factory = f.Heartofgold(self, 'heartofgold_factory')

        # Launches
        self.launchpad = l.EarthLaunchPad(self, 'earth_launchpad')
