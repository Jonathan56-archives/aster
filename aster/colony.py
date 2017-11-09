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

    def set_initial(self, structure, parameter):
        """Get initial value for structures"""
        mask = ((self.sim.initial.colony == self.name) &
                (self.sim.initial.structure == structure) &
                (self.sim.initial.parameter == parameter))

        # Check that only one value is selected with the mask
        assert len(self.sim.initial[mask].value) == 1
        return self.sim.initial[mask].value.iloc[0]

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
        """Create Mars"""
        super(Mars, self).__init__(simulation, 'mars')
        # Store for Heartofgolds
        self.heartofgold_storage = s.Heartofgold(self, items=False)

        # Launches
        self.launchpad = l.MarsLaunchPad(self)


class Earth_LEO(Colony):
    def __init__(self, simulation):
        """Create Earth"""
        super(Earth_LEO, self).__init__(simulation, 'earth_LEO')

        # Create storage for heartofgold
        self.tank_storage = s.Tank(self, items=False)


class Earth(Colony):
    def __init__(self, simulation):
        """Create Earth"""
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
        self.booster_graveyard = s.Booster(self, items=False, suffix='_graveyard')
        self.tank_graveyard = s.Tank(self, items=False, suffix='_graveyard')
        self.heartofgold_graveyard = s.Heartofgold(self, items=False, suffix='_graveyard')

        # Set factories
        self.propelant_factory = f.Propellant(self)
        self.booster_factory = f.Booster(self)
        self.tank_factory = f.Tank(self)
        self.heartofgold_factory = f.Heartofgold(self)

        # Launches
        self.launchpad = l.EarthLaunchPad(self)
