import pylab
import networkx as nx
import numpy as np


class net_drawer(object):

    '''
    this class allows one to staticaly draw the topology of 
    a neural network while dynamically updating the states of 
    the network.
    '''

    
    def __init__(self,adj_matrix):

        self.G = nx.from_numpy_matrix(adj_matrix)  #the networkx graph class to e
        self.fig = pylab.figure()  # the graph will drawn in this figure
       # pylab.show() 
        
    def get_on_ndes(self,state):
        av = np.average(states) 
        sd = np.std(states)
        threshold = av+std
        return [i for i,t in map(lambda x: x > threshold, states) if t] 

    def update(self,states):
        turned_on = self.mapthreshold()
        self.fig.clear()
        nx.draw_networkx_nodes(G,pos,
                       nodelist=[0,1,2,3],
                       node_color='r',
                       node_size=500,
                   alpha=0.8)    



drawer = net_drawer(np.matrix([[1,2],[3,4]]))
print drawer.get_on_ndes([1,2,3,4,5,9,6,4,22,40])

