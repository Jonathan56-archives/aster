

class Factory(object):
    def __init__(self, colony, name):
        self.sim = body.sim
        self.colony = colony

        # Initialize factory parameters
        self.production = colony.set_initial(name, 'production')
        self.rate = colony.set_initial(name, 'rate')


class Propellant(Factory):
    def __inti__(self, colony):
        super(Factory, self).__init__(colony, 'propelant_factory')

    def start(self):
        while True:
            yield self.sim.env.timeout(self.rate)
            yield self.colony.propelant_container.put(self.rate)


class Booster(Factory):
    def __inti__(self, colony):
        super(Factory, self).__init__(colony, 'booster_factory')

    def start(self):
        while True:
            yield self.sim.env.timeout(self.rate)
            yield self.colony.booster_storage.put(self.rate)


class Tank(Factory):
    def __inti__(self, colony):
        super(Factory, self).__init__(colony, 'tank_factory')

    def start(self):
        while True:
            yield self.sim.env.timeout(self.rate)
            yield self.colony.tank_storage.put(self.rate)


class Heartofgold(Factory):
    def __inti__(self, colony):
        super(Factory, self).__init__(colony, 'heartofgold_factory')

    def start(self):
        while True:
            yield self.sim.env.timeout(self.rate)
            yield self.colony.heartofgold_storage.put(self.rate)
