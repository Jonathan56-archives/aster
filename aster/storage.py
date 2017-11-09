import simpy
import spacecraft as sc

class Storage(simpy.resources.store.Store):
    def __init__(self, colony, name, *args, **kwargs):
        # Reference to the simulation
        self.sim = colony.sim
        self.colony = colony
        self.name = name

        # Initialize all the simpy variables
        super(Storage, self).__init__(self.sim.env, *args, **kwargs)

    def get(self, *args, **kwargs):
        obj = super(Storage, self).get(*args, **kwargs)
        self.sim.logger.log(
            self, self.get_message, key=self.get_key,
            value=len(self.items))
        return obj

    def put(self, *args, **kwargs):
        before = len(self.items)
        obj = super(Storage, self).put(*args, **kwargs)
        assert before == len(self.items) - 1
        self.sim.logger.log(
            self, self.put_message, key=self.put_key,
            value=len(self.items))
        return obj


class Booster(Storage):
    def __init__(self, colony, items=True, suffix='', *args, **kwargs):
        super(Booster, self).__init__(colony, 'booster_storage' + suffix, *args, **kwargs)

        # Initialize storage
        if items:
            self.items = (
                [sc.Booster(self.sim) for i in
                range(0, int(self.colony.set_initial('booster_storage', 'stock')))])

        # Log message
        self.get_message = 'Get booster from ' + self.colony.name + ' ' + suffix
        self.get_key = 'get_booster_' + self.colony.name + suffix
        self.put_message = 'Put booster from '+ self.colony.name + ' ' + suffix
        self.put_key = 'put_booster_' + self.colony.name + suffix


class Tank(Storage):
    def __init__(self, colony, items=True, suffix='', *args, **kwargs):
        super(Tank, self).__init__(colony, 'tank_storage' + suffix, *args, **kwargs)

        # Initialize storage
        if items:
            self.items = (
                [sc.Tank(self.sim) for i in
                range(0, int(self.colony.set_initial('tank_storage', 'stock')))])

        # Log message
        self.get_message = 'Get tank from ' + self.colony.name + ' ' + suffix
        self.get_key = 'get_tank_' + self.colony.name + suffix
        self.put_message = 'Put tank from '+ self.colony.name + ' ' + suffix
        self.put_key = 'put_tank_' + self.colony.name + suffix


class Heartofgold(Storage):
    def __init__(self, colony, items=True, suffix='', *args, **kwargs):
        super(Heartofgold, self).__init__(colony, 'heartofgold_storage' + suffix, *args, **kwargs)

        # Initialize storage
        if items:
            self.items = (
                [sc.Heartofgold(self.sim) for i in
                range(0, int(self.colony.set_initial('heartofgold_storage', 'stock')))])

        # Log message
        self.get_message = 'Get heartofgold from ' + self.colony.name + ' ' + suffix
        self.get_key = 'get_heartofgold_' + self.colony.name + suffix
        self.put_message = 'Put heartofgold from '+ self.colony.name + ' ' + suffix
        self.put_key = 'put_heartofgold_' + self.colony.name + suffix
