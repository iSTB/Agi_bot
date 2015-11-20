import math
import os
from neat import population
from neat.config import Config
from neat.nn import nn_pure as nn

class neat(object):


    def __init__(self):
        self.current_nn = None        
        self.sensor_values = None
        self.change = False
    def get_motor(self,sensors):

        if self.current_nn != None: 
            return self.current_nn.sactivate(sensors)

    def set_sensors(self,senors):
        self.sensors_values = sensor_values
    
    def fit_func(sensors_before, sensors_after):

        min_sensor, min_index = min((val, idx) for (idx, val) in enumerate(sensors_before) if idx != 0)

        min_sensor_diff = sensors_after[min_index] - min_sensor
        t_other_sens_diff = 0.0
        for i in xrange(len(sensors_before)):
            if i != min_index:
                t_other_sens_diff += sensors_after[i] - sensors_before[i]        
        
        av_other_sens_diff = t_other_sens_diff/(len(sensors_after) - 1.0)

        return (av_other_sens_diff + min_sensor_diff)/2.0



    def eval_fitness(self,genomes):
        for g in genomes:
            net = nn.create_fast_feedforward_phenotype(g)
            self.curr_nn = net

            start_sensors  = self.current_sensors  #this will be the current sensors from the robot
            
            ##LET ROBOT RUN HERE

            finish_sensors = self.current_sensors
            g.fitness = fit_func(curr_sensors,after_sensors) 

    def run(self):
        local_dir = os.path.dirname(__file__)
        config = Config(os.path.join(local_dir, 'evolve_config'))

        pop = population.Population(config)
        pop.epoch(eval_fitness, 300)


        winner = pop.most_fit_genomes[-1]
        
        self.current_nn = winner

        print 'Number of evaluations: %d' % winner.ID
      
        # Verify network output against training data.
        print '\nBest network output:'
        net = nn.create_fast_feedforward_phenotype(winner)




if  __name__ == '__main__':
    

    run()
