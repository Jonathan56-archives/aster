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


# class Monitoring(object):
#     def __init__(self, simulation):
#         self.sim = simulation
#         self.rate = 30 * 24 * 60 * 60
#
#     def plot(self):
#         # Create a matrix of plots
#         nb_plots = 6
#         nb_columns = 3
#         nb_rows = 2
#         f, axarr = plt.subplots(nb_rows, nb_columns, figsize=(20, 8))
#
#         # # Plot propellant tank
#         # data = self.sim.log[self.sim.log.key == 'earth_propellant']
#         # axarr[0, 0].plot(data.datetime, data.value)
#         # axarr[0, 0].set_title('earth_propellant')
#
#         # Plot booster storage
#         data = self.sim.log[self.sim.log.key == 'get_booster_earth']
#         axarr[0, 1].plot(data.datetime, data.value)
#         axarr[0, 1].set_title('earth_booster')
#
#         # Plot heartofgold storage
#         data = self.sim.log[self.sim.log.key == 'get_heartofgold_earth']
#         axarr[0, 2].plot(data.datetime, data.value)
#         axarr[0, 2].set_title('earth_heartofgold')
#
#         # Plot tank storage
#         data = self.sim.log[self.sim.log.key == 'get_tank_earth']
#         axarr[1, 0].plot(data.datetime, data.value)
#         axarr[1, 0].set_title('earth_tank')
#
#         # # Plot number of tank in orbit
#         # data = self.sim.log[self.sim.log.key == 'leo_tank']
#         # axarr[1, 1].plot(data.datetime, data.value)
#         # axarr[1, 1].set_title('leo_tank')
#         #
#         # # Plot number of heartofgold arrived on Mars
#         # data = self.sim.log[self.sim.log.key == 'mars_heartofgold']
#         # axarr[1, 2].plot(data.datetime, data.value)
#         # axarr[1, 2].set_title('mars_heartofgold')
#         plt.show()
#
#     def __str__(self):
#         return "Monitor"
