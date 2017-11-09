import datetime as dt
import matplotlib.pyplot as plt
from functools import wraps
import seaborn


class Logger(object):
    def __init__(self, simulation):
        self.sim = simulation

    def log(self, this, message,
            key='', value=0, level='INFO', location=None):
        self.sim.log.append({
            'level': level,
            'datetime': dt.timedelta(seconds=self.sim.env.now) + self.sim.start,
            'source': this,
            'location': location,
            'message': message,
            'key': key,
            'value': value})
