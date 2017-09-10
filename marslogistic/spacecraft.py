

class Spacecraft(object):
    def __init__(self, simulation, name):
        self.sim = simulation
        self.name = name

        # Parameters
        self.number_of_launch = 0
        self.maximum_nb_of_launch = 10

    def __str__(self):
        return "Spacecraft"


class Booster(Spacecraft):
    def __init__(self, simulation):
        super(Booster, self).__init__(simulation, 'booster')
        self.maximum_nb_of_launch = 1

    def launch(self, launched):
        # Launch
        self.number_of_launch += 1
        launched.number_of_launch += 1

        # Log launch
        self.sim.logger.log(
            self, 'Booster launched', key='booster_launched', value=1)

        # Separate with the launched
        yield self.sim.env.process(launched.separate_from_booster())

        # Come back on earth
        yield self.sim.env.process(self.come_back_to_earth())

    def come_back_to_earth(self):
        # Come back down
        if self.number_of_launch < self.maximum_nb_of_launch:
            # Re-use tank later
            self.sim.logger.log(
                self, 'Booster ready for reuse', key='booster_reuse', value=1)
            yield self.sim.earth.booster_storage.put(self)
        else:
            # Throw booster into the old booster pile
            self.sim.logger.log(
                self, 'Booster destroyed', key='booster_destroyed', value=1)
            yield self.sim.earth.booster_graveyard.put(self)


class Tank(Spacecraft):
    def __init__(self, simulation):
        super(Tank, self).__init__(simulation, 'tank')
        self.maximum_nb_of_launch = 1

    def separate_from_booster(self):
        # Log launch
        self.sim.logger.log(
            self, 'Tank launched', key='tank_launched', value=1)

        # Add some tank on LEO
        yield self.sim.earth.tank_storage_in_LEO.put(self)

    def come_back_to_earth(self):
        # Come back down
        if self.number_of_launch < self.maximum_nb_of_launch:
            # Re-use tank later
            self.sim.logger.log(
                self, 'Tank ready for reuse', key='tank_reuse', value=1)
            yield self.sim.earth.tank_storage.put(self)
        else:
            # Throw booster into the old booster pile
            self.sim.logger.log(
                self, 'Tank destroyed', key='tank_destroyed', value=1)
            yield self.sim.earth.tank_graveyard.put(self)


class Heartofgold(Spacecraft):
    def __init__(self, simulation):
        super(Heartofgold, self).__init__(simulation, 'heartofgold')

        # Parameters
        self.number_of_refuel = 5

    def separate_from_booster(self):
        # Log launch
        self.sim.logger.log(
            self, 'Heartofgold launched', key='heartofgold_launched', value=1)

        # Start refueling process
        yield self.sim.env.process(self.refuel_in_orbit())

        # Head to Mars
        yield self.sim.env.timeout(6 * 30 * 24 * 60 * 60)
        yield self.sim.mars.heartofgold_storage.put(self)

    def refuel_in_orbit(self):
        # Remove 5 tanks from LEO
        for index in range(0, self.number_of_refuel):
            # Get a tank
            tank = yield self.sim.earth.tank_storage_in_LEO.get()
            yield self.sim.env.process(tank.come_back_to_earth())

    def come_back_to_earth(self):
        pass
