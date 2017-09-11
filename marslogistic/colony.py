import factory as f
import launchpad as l
import spacecraft as sc
import monitoring as m
import storage as s
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


class Earth(Colony):
    def __init__(self, simulation):
        """Create Earth | Add ressources and processes within env"""
        super(Earth, self).__init__(simulation, 'earth')

        # Containers
        # Ground level propellant reserves
        self.propelant_container = simpy.Container(
            self.sim.env, init=self.set_initial('propellant_container', 'stock'))

        # Storages
        # Ground level spacecraft storages
        self.booster_storage = s.Booster(self)
        self.tank_storage = s.Tank(self)
        self.heartofgold_storage = s.Heartofgold(self)

        # LEO tank storage
        self.tank_storage_in_LEO = simpy.Store(self.sim.env)

        # Old spacecraft recycling
        self.booster_graveyard = simpy.Store(self.sim.env)
        self.tank_graveyard = simpy.Store(self.sim.env)
        self.heartofgold_graveyard = simpy.Store(self.sim.env)

        # Set factories
        self.propelant_factory = f.Propellant(self)
        self.booster_factory = f.Booster(self)
        self.tank_factory = f.Tank(self)
        self.heartofgold_factory = f.Heartofgold(self)

        # Launches
        self.launchpad = l.EarthLaunchPad(self)

    def set_initial(self, structure, parameter):
        """Get initial value for structures"""
        mask = ((self.sim.initial.colony == 'earth') &
                (self.sim.initial.structure == structure) &
                (self.sim.initial.parameter == parameter))

        # Check that only one value is selected with the mask
        assert len(self.sim.initial[mask].value) == 1
        return self.sim.initial[mask].value.iloc[0]
