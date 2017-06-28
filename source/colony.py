import factory as f
import storage as s
import launchpad as l
import spacecraft as sc
import simpy


class Colony(object):
    def __init__(self, simulation, name):
        self.sim = simulation
        self.name = name

    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        return setattr(self, name, value)

    def __delitem__(self, name):
        return delattr(self, name)

    def __contains__(self, name):
        return hasattr(self, name)


class Earth(Colony):
    def __init__(self, simulation):
        """Create Earth | Add ressources and processes within env"""
        super(Colony, self).__init__(simulation, 'earth')

        ## Containers
        self.propelant_container = simpy.Container(
            self.sim.env, init=self.initial('propelant_container', 'init'))

        ## Storages
        self.booster_storage = simpy.Store(self.sim.env)
        self.booster_storage.items = (
            [sc.Booster() for i in range(0, self.initial('booster_storage', 'init'))])
        self.tank_storage = simpy.Store(self.sim.env)
        self.tank_storage.items = (
            [sc.Tank() for i in range(0, self.initial('tank_storage', 'init'))])
        self.heartofgold_storage = simpy.Store(self.sim.env)
        self.heartofgold_storage.items = (
            [sc.Heartofgold() for i in range(0, self.initial('heartofgold_storage', 'init'))])

        ## Processes
        # Factories
        self.propelant_factory = f.Propellant(self, 'propelant_factory')
        self.booster_factory = f.Booster(self, 'booster_factory')
        self.tank_factory = f.Tank(self, 'tank_factory')
        self.heartofgold_factory = f.Heartofgold(self, 'heartofgold_factory')

        # Launches
        self.launchpad = l.EarthLaunchPad(self, 'earth_launchpad')

    def initial(self, structure, parameter):
        """Get initial value for structures"""
        mask = (self.sim.initial.colony == 'earth' &
                self.sim.intial.structure == structure &
                self.sim.intial.structure == parameter &)
        return self.sim.initial[mask].value.iloc[0]
