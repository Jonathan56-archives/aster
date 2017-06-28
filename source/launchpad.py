

class LaunchPad(object):
    def __init__(self, colony, name):
        self.colony = colony
        self.name = name


class EarthLaunchPad(LaunchPad):
    def __init__(self, colony, name):
        super(LaunchPad, self).__init__(colony, name)
