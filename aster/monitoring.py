import datetime as dt
import matplotlib.pyplot as plt
from functools import wraps
import seaborn
import pandas


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


class LogParser(object):
    def __init__(self, log_filename):
        self.log_filename = log_filename
        self.log = pandas.read_csv(log_filename, index_col=0, parse_dates=[1])
        self.launching_dates = False

    def get(self, keys, freq='10D'):
        """Create a time series with keys"""
        # Filter keys
        data = self.log[self.log.key.isin(keys)]

        # Get unique dates
        x_set = pandas.unique(data['datetime'])

        # Get last value for each unique date
        data_set = []
        for x in x_set:
            data_set.append(data[data['datetime'] == x].iloc[-1])
        assert(len(data_set) != 0)

        # Recreate a dataframe and resample to 1 day
        xy = pandas.DataFrame(data_set)[['datetime', 'value']]
        xy = xy.set_index(['datetime'])
        xy = xy.resample(freq).ffill()
        return xy

    def get_cummulative(self, keys, freq='10D'):
        # Filter keys
        data = self.log[self.log.key.isin(keys)]
        assert(len(data) != 0)

        # Count number per unique date
        data = data.groupby('datetime').count()

        # New data vector to cum and resample
        xy = data[['value']].copy()
        xy['value'] = xy['value'].cumsum()
        xy = xy.resample(freq).ffill()
        return xy

    def list_keys(self):
        keys = pandas.unique(self.log['key'])
        print(keys)

    def plot_launching_window(self):
        """Plot line at window opening"""
        # Find date of window opening
        if not self.launching_dates:
            self.launching_dates = self.log[self.log.key == 'launch_window_open'].datetime.tolist()

        # Plot lines
        for date in self.launching_dates:
            plt.axvline(date, linewidth=2, color='r', alpha=0.5)
