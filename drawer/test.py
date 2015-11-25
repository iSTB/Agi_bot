import random
import pylab
from matplotlib.pyplot import pause
import networkx as nx
pylab.ion()

graph = nx.Graph()
node_number = 0
graph.add_node(node_number, Position=(random.randrange(0, 100), random.randrange(0, 100)))


def get_fig(fig):
    fig.clear()
    global node_number
    node_number += 1
    graph.add_node(node_number, Position=(random.randrange(0, 100), random.randrange(0, 100)))
    graph.add_edge(node_number, random.choice(graph.nodes()))
    nx.draw(graph, pos=nx.get_node_attributes(graph,'Position'))
    return fig

num_plots = 50;
pylab.show()

fig = pylab.figure()
for i in range(num_plots):

    fig = get_fig(fig)
    fig.canvas.draw()
    pylab.draw()
    pause(2)
    
#pylab.close(fig)
