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
                # Add Booster and heartofgold
                self.lineup = [self.colony.booster_storage.get(),
                               self.colony.heartofgold_storage.get()]

                # Prepare more boosters for the propellant tanks
                self.lineup.extend(
                    [self.colony.booster_storage.get() for i in range(0, 5)])

                # Get the tanks
                self.lineup.extend(
                    [self.colony.tank_storage.get() for i in range(0, 5)])

                # Wait for all the conditions to be lineup and ready
                wait_for_spacecrafts = AllOf(self.sim.env, self.lineup)
                yield wait_for_spacecrafts
                spacecrafts = wait_for_spacecrafts.value

                # Fire the tanks
                for index in range(0, 5):
                    self.sim.env.process(
                        spacecrafts[self.lineup[2 + index]].launch(
                            spacecrafts[self.lineup[2 + 5 + index]]))

                # Fire the heartofgold
                self.sim.env.process(spacecrafts[self.lineup[0]].launch(
                    spacecrafts[self.lineup[1]]))
        except:
            # Close window and recall all spaceships to their stores
            for req in self.lineup:
                if req.processed: # tests if the request completed
                    yield req.resource.put(req.value)
                else:
                    # Log what's missing
                    self.sim.logger.log(
                        self, 'Missing ' + str(req) + ' before launch',
                        key='missing_for_launch')

                    # Cancel request
                    req.cancel()
