

class Spacecraft(object):
    def __init__(self, simulation, name):
        self.sim = simulation
        self.name = name

        # Parameters
        self.number_of_launch = 0
        self.maximum_nb_of_launch = 10


class Booster(Spacecraft):
    def __init__(self, simulation):
        super(Spacecraft, self).__init__(simulation, 'booster')

    def launch(self, launched):
        # Launch
        self.number_of_launch += 1
        launched.number_of_launch += 1

        # Separate with the launched
        yield self.sim.env.process(launched.separate_from_booster())

        # Come back on earth
        yield self.sim.env.process(self.come_back_to_earth())

    def come_back_to_earth(self):
        # Come back down
        if self.number_of_launch < self.maximum_nb_of_launch:
            # Re-use tank later
            yield self.sim.earth.booster_storage.put(self)
        else:
            # Throw booster into the old booster pile
            yield self.sim.earth.booster_recycling.put(self)


class Tank(Spacecraft):
    def __init__(self, simulation):
        super(Spacecraft, self).__init__(simulation, 'tank')

    def separate_from_booster(self):
        # Add some tank on LEO
        yield self.simulation.eart.tank_storage_in_LEO.put(self)

    def come_back_to_earth(self):
        # Come back down
        if self.number_of_launch < self.maximum_nb_of_launch:
            # Re-use tank later
            yield self.sim.earth.tank_storage.put(self)
        else:
            # Throw booster into the old booster pile
            yield self.sim.earth.tank_recycling.put(self)


class Heartofgold(Spacecraft):
    def __init__(self, simulation):
        super(Spacecraft, self).__init__(simulation, 'heartofgold')

        # Parameters
        self.number_of_refuel = 5

    def separate_from_booster(self):
        # Start refueling process
        yield self.sim.env.process(self.refuel_in_orbit())

        # Head to Mars
        yield self.sim.env.timeout(2 * 365 * 24 * 60 * 60)

    def refuel_in_orbit(self):
        # Remove 5 tanks from LEO
        for index in range(0, self.number_of_refuel):
            # Get a tank
            tank = yield self.sim.earth.tank_storage_in_LEO.get()
            yield self.sim.env.process(tank.come_back_to_earth())

    def come_back_to_earth(self):
        pass
