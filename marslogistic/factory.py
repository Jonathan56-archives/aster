

class Factory(object):
    def __init__(self, colony, name):
        self.sim = colony.sim
        self.colony = colony

        # Initialize factory parameters
        self.production = colony.set_initial(name, 'production')
        self.rate = colony.set_initial(name, 'rate')


class Propellant(Factory):
    def __init__(self, colony):
        super(Propellant, self).__init__(colony, 'propellant_factory')

        # Start factory
        self.sim.env.process(self.start())

    def start(self):
        while True:
            yield self.sim.env.timeout(self.rate)
            yield self.colony.propelant_container.put(self.rate)


class Booster(Factory):
    def __init__(self, colony):
        super(Booster, self).__init__(colony, 'booster_factory')

        # Start factory
        self.sim.env.process(self.start())

    def start(self):
        while True:
            yield self.sim.env.timeout(self.rate)
            yield self.colony.booster_storage.put(self.rate)


class Tank(Factory):
    def __init__(self, colony):
        super(Tank, self).__init__(colony, 'tank_factory')

        # Start factory
        self.sim.env.process(self.start())

    def start(self):
        while True:
            yield self.sim.env.timeout(self.rate)
            yield self.colony.tank_storage.put(self.rate)


class Heartofgold(Factory):
    def __init__(self, colony):
        super(Heartofgold, self).__init__(colony, 'heartofgold_factory')

        # Start factory
        self.sim.env.process(self.start())

    def start(self):
        while True:
            yield self.sim.env.timeout(self.rate)
            yield self.colony.heartofgold_storage.put(self.rate)
