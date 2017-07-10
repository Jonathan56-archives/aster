from __future__ import division
import pandas
import marslogistic

# Read timeline
timeline = pandas.read_excel('timeline.xlsx', sheetname=None)

# Create simulation
simulation = marslogistic.Simulation(
    'db', timeline['initialization'], 'timeline')

# Start simulation
simulation.run()
