

class Factory(object):

    def __init__(self, colony, name):
        self.sim = body.sim
        self.colony = colony

        # Initialize factory parameters
        self.production_rate = colony[name, ‘production_rate’]
        self.timestep =


class Propellant(Factory):
    def __inti__(self, colony, name):
        super(Factory, self).__init__(colony, name)

        # Specific parameters to propellant plants
        self.storage = self.colony.propelant_storage


    def start(self):
        yield self.sim.env.timeout(self.timestep)
