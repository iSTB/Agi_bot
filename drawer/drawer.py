import matplotlib.pyplot as pylab
from matplotlib.pyplot import pause
import networkx as nx
import numpy as np
import matplotlib 
matplotlib.rcParams['toolbar'] = 'None'
class net_drawer(object):

    '''
    this class allows one to staticaly draw the topology of 
    a neural network while dynamically updating the states of 
    the network.
    '''

    
    def __init__(self,adj_matrix):
        
        self.G = nx.from_numpy_matrix(adj_matrix)
        #print self.G.edges(data=True)  #the networkx graph class to e
        self.pos=nx.spring_layout(self.G)
        self.fig = pylab.figure()  # the graph will drawn in this figure
        mng = pylab.get_current_fig_manager()
        mng.window.showMaximized()
       
        
        pylab.ion()
        self.fig.patch.set_facecolor('black')
        #mng = self.fig.get_current_fig_manager()
        
        #mng.frame.Maximize(True)
        self.edge_width = [abs(d['weight'])*25 for (u,v,d) in self.G.edges(data=True)]
        
        #ax = pylab.gca()
        #print self.edge_width
        #ax.yaxis.set_visible(False)
        #ax.xaxis.set_visible(False)
    def get_on_nodes(self,states):
        av = np.average(states) 
        std = np.std(states)
        threshold = av
        return [i for i,t in enumerate(states) if t > threshold] 

    def update(self,states):
        turned_on = self.get_on_nodes(states)
        # print "turned_on:", turned_on
        # print "states:", states
        turned_off = [i for i,v in enumerate(states) if i not in turned_on]
        self.fig.clear()
        ax = pylab.gca()
        ax.yaxis.set_visible(False)
        ax.xaxis.set_visible(False)
        ax.set_axis_bgcolor('black')
        nx.draw_networkx_nodes(self.G,self.pos,
                       nodelist=turned_on,
                       node_color='white',
                       node_size=30,
                       alpha=0.85)    


        nx.draw_networkx_nodes(self.G,self.pos,
                       nodelist=turned_off,
                       node_color='white',
                       node_size=20,
                       alpha=0.25)

        nx.draw_networkx_edges(self.G,self.pos,
                      width=self.edge_width,alpha=0.6,edge_color='white')
        pylab.tight_layout()
        pause(2)
    def close(self,):
      pylab.close()
if __name__=="__main__":
  drawer = net_drawer(np.matrix([[0.7,0.1],[.91,0.5]]))
  import time
  time.sleep(2)
  # while True:
  for _ in range(10):
      drawer.update([100,1])
      drawer.update([30,100])
  drawer.close()
