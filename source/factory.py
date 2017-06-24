

class Factory(object):

    def __init__(self, body, name):
        self.sim = body.sim
        self.body = body

        # Initialize factory parameters
        self.production_rate = body[name, ‘production_rate’]
        self.timestep = ...


class Propellant(Factory):
    def __inti__(self, body, name):
        self._super(body, name)

        # Specific parameters to propellant plants
        self.storage = self.body.propelant_storage


    def start(self):
        yield self.sim.env.timeout(self.timestep)
