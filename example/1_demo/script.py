from __future__ import division
import pandas
import datetime as dt
import marslogistic.simulation as m

# Read timeline
timeline = pandas.read_excel('timeline.xlsx')

# Create simulation
simulation = m.Simulation('db', timeline)

# Start simulation
simulation.end = dt.datetime(2028, 1, 1, 0, 0, 0)
simulation.run()
