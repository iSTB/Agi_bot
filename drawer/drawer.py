import matplotlib.pyplot as pylab
from matplotlib.pyplot import pause
import networkx as nx
import numpy as np
import matplotlib

class net_drawer(object):

    '''
    this class allows one to staticaly draw the topology of 
    a neural network while dynamically updating the states of 
    the network.
    '''

    
    def __init__(self,adj_matrix):
        
        self.G = nx.from_numpy_matrix(adj_matrix)  #the networkx graph class to e
        self.pos=nx.spring_layout(self.G)
        self.fig = pylab.figure()  # the graph will drawn in this figure
        pylab.ion()
        #ax = pylab.gca()

        #ax.yaxis.set_visible(False)
        #ax.xaxis.set_visible(False)
    def get_on_nodes(self,states):
        av = np.average(states) 
        std = np.std(states)
        threshold = av
        return [i for i,t in enumerate(map(lambda x: x > threshold, states)) if t] 

    def update(self,states):
        turned_on = self.get_on_nodes(states)
        print turned_on
        turned_off = [i for i,v in enumerate(states) if i not in turned_on]
        self.fig.clear()
        ax = pylab.gca()
         
        ax.yaxis.set_visible(False)
        ax.xaxis.set_visible(False)
        nx.draw_networkx_nodes(self.G,self.pos,
                       nodelist=turned_on,
                       node_color='r',
                       node_size=700,
                   alpha=1)    


        nx.draw_networkx_nodes(self.G,self.pos,
                       nodelist=turned_off,
                       node_color='w',
                       node_size=700,
                       alpha=1)

        nx.draw_networkx_edges(self.G,self.pos,
                      width=2,alpha=0.5,edge_color='black')
 
        pause(2)

drawer = net_drawer(np.matrix([[1,0],[1,0]]))
import time
time.sleep(2)
while True:
    drawer.update([100,1])
    drawer.update([30,100])

