from simpy.events import AllOf


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

        # Launchpad vehicles
        self.lineup = []
        self.h_booster = False
        self.heartofgold = False
        self.t_booster = False
        self.tank = False

    def start(self):
        """Start the launching procedure"""
        try:
            while True:
                # Event list
                self.lineup = []

                # Get the heartofgold and booster
                self.h_booster = yield self.colony.booster_storage.get()
                self.heartofgold = yield self.colony.heartofgold_storage.get()

                # Get 5 tanks and booster
                for index in range(0, 5):
                    self.t_booster = yield self.colony.booster_storage.get()
                    self.tank = yield self.colony.tank_storage.get()
                    self.sim.env.process(self.t_booster.launch(self.tank))
                    self.t_booster = False
                    self.tank =  False
                # !!!!!!!!!!!!!!!! CREATE AN ARRAY AND THEN LAUNCH ALL
                # !!!!!!! yield for all of them

                # Launch the heartofgold
                self.sim.env.process(self.h_booster.launch(self.heartofgold))
                self.h_booster = False
                self.heartofgold = False

        except:
            # Window just closed stop the launches
            # Put back vehicle ready for launches back in store
            if self.h_booster:
                yield self.colony.booster_storage.put(self.h_booster)

            if self.heartofgold:
                yield self.colony.heartofgold_storage.put(self.heartofgold)

            if self.t_booster:
                yield self.colony.booster_storage.put(self.t_booster)

            if self.tank:
                yield self.colony.tank_storage.put(self.tank)

    def launch_procedure(self):
        pass

    def clear_launchpad(self):
        pass
