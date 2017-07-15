

class LaunchPad(object):
    def __init__(self, colony, name):
        self.sim = colony.sim
        self.colony = colony
        self.name = name

    def __str__(self):
        return "Launchpad"

class EarthLaunchPad(LaunchPad):
    def __init__(self, colony):
        super(EarthLaunchPad, self).__init__(colony, 'earth_launchpad')

        # Start launchpad activities
        self.sim.env.process(self.start())

    def start(self):
        while True:
            # Wait for 2 years
            yield self.sim.env.timeout(int(2.1 * 365 * 24 * 60 * 60))
            window_start = self.sim.env.now
            window_end = window_start + 30 * 24 * 60 * 60
            self.sim.logger.log(self, 'Launching window opened')

            while self.sim.env.now < window_end:
                # Get 5 tanks and booster
                for index in range(0, 5):
                    booster = yield self.colony.booster_storage.get()
                    tank = yield self.colony.tank_storage.get()
                    self.sim.env.process(booster.launch(tank))

                # Get the heartofgold on its way
                booster = yield self.colony.booster_storage.get()
                heartofgold = yield self.colony.heartofgold_storage.get()
                self.sim.env.process(booster.launch(heartofgold))
