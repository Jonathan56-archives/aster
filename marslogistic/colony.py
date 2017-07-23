import factory as f
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


class Mars(Colony):
    def __init__(self, simulation):
        """Create Earth | Add ressources and processes within env"""
        super(Mars, self).__init__(simulation, 'mars')

        # Store for Heartofgolds
        self.heartofgold_storage = simpy.Store(self.sim.env)

    def log(self):
        """Log colony status"""
        # Log the number of ship on Mars
        self.sim.logger.log(
            self, 'Heartofgolds on Mars', key='mars_heartofgold',
            level='DATA', value=len(self.heartofgold_storage.items))


class Earth(Colony):
    def __init__(self, simulation):
        """Create Earth | Add ressources and processes within env"""
        super(Earth, self).__init__(simulation, 'earth')

        # Set container and stores
        self.set_container_and_store()

        # Set factories
        self.propelant_factory = f.Propellant(self)
        self.booster_factory = f.Booster(self)
        self.tank_factory = f.Tank(self)
        self.heartofgold_factory = f.Heartofgold(self)

        # Launches
        self.launchpad = l.EarthLaunchPad(self)

    def log(self):
        """Log colony status"""
        # Log propellant stocks
        self.sim.logger.log(
            self, 'Propellant on Earth', key='earth_propellant',
            level='DATA', value=self.propelant_container.level)

        # Log Active Booster stocks
        self.sim.logger.log(
            self, 'Active booster on Earth', key='earth_booster',
            level='DATA', value=len(self.booster_storage.items))

        # Log Active Tank stocks
        self.sim.logger.log(
            self, 'Active tank on Earth', key='earth_tank',
            level='DATA', value=len(self.tank_storage.items))
        self.sim.logger.log(
            self, 'Active tank on LEO', key='leo_tank',
            level='DATA', value=len(self.tank_storage_in_LEO.items))

        # Log Active Heartofgold stocks
        self.sim.logger.log(
            self, 'Active heartofgold on Earth', key='earth_heartofgold',
            level='DATA', value=len(self.heartofgold_storage.items))

    def set_container_and_store(self):
        """Set Containers and Stores"""
        # Containers
        # Ground level propellant reserves
        self.propelant_container = simpy.Container(
            self.sim.env, init=self.set_initial('propellant_container', 'stock'))

        # Storages
        # Ground level spacecraft storages
        self.booster_storage = simpy.Store(self.sim.env)
        self.booster_storage.items = (
            [sc.Booster(self.sim) for i in range(0, self.set_initial('booster_storage', 'stock'))])
        self.tank_storage = simpy.Store(self.sim.env)
        self.tank_storage.items = (
            [sc.Tank(self.sim) for i in range(0, self.set_initial('tank_storage', 'stock'))])
        self.heartofgold_storage = simpy.Store(self.sim.env)
        self.heartofgold_storage.items = (
            [sc.Heartofgold(self.sim) for i in range(0, self.set_initial('heartofgold_storage', 'stock'))])

        # LEO tank storage
        self.tank_storage_in_LEO = simpy.Store(self.sim.env)

        # Old spacecraft recycling
        self.booster_graveyard = simpy.Store(self.sim.env)
        self.tank_graveyard = simpy.Store(self.sim.env)
        self.heartofgold_graveyard = simpy.Store(self.sim.env)

    def set_initial(self, structure, parameter):
        """Get initial value for structures"""
        mask = ((self.sim.initial.colony == 'earth') &
                (self.sim.initial.structure == structure) &
                (self.sim.initial.parameter == parameter))

        # Check that only one value is selected with the mask
        assert len(self.sim.initial[mask].value) == 1
        return self.sim.initial[mask].value.iloc[0]
