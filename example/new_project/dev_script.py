from __future__ import division
import pandas
import datetime as dt
import aster.factory
import aster.storage
import networkx
from networkx.readwrite import json_graph
import matplotlib.pylab as plt

nodes = [
    {
        "id": 0,
        "module": aster.factory.Booster,
        "group": "earth"
    },
    {
        "id": 1,
        "module": aster.storage.Booster,
        "group": "earth"
    }
]

links = [
    {
        "source": 0,
        "target": 1,
        "description": "send booster to storage",
    }
]

graph = json_graph.node_link_graph({'nodes': nodes, 'links': links})

# Visualize the network:
networkx.draw_networkx(graph)
plt.show()

# # Read timeline
# timeline = pandas.read_excel('timeline.xlsx')
#
# # Create simulation
# simulation = m.Simulation('db', timeline)
# simulation.end = dt.datetime(2030, 12, 1, 0, 0, 0)
#
# # Start simulation
# simulation.run()
