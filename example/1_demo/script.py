from __future__ import division
import pandas
import marslogistic.simulation as m

# Read timeline
timeline = pandas.read_excel('timeline.xlsx', sheetname=None)

# Create simulation
simulation = m.Simulation(
    'db', timeline['initialization'], 'timeline')

# Start simulation
simulation.run()
