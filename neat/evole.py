import math
import os
from neat import population
from neat.config import Config
from neat.nn import nn_pure as nn
from time import sleep
class neat(object):


    def __init__(self):
        self.current_nn = None        
        self.sensor_values = [0,0,0,0,0,0]
        self.change = False
        self.on = False


    def turn_on(self):
        self.on = True

    def turn_off(self):
        self.on = False
    def get_motor(self,sensors):
        #print sensors
        if self.current_nn != None: 
            v = self.current_nn.sactivate(sensors)
            # bin_size = 1/9.
            # val = round(v/bin_size)
            # ret = [0]*9
            # ret[val] = 1

            return v

    def set_sensors(self,senors):
        self.sensors_values = senors
    
    def fit_func(self,sensors_before, sensors_after):

        min_sensor, min_index = min((val, idx) for (idx, val) in enumerate(sensors_before) if idx != 0)
        
        min_sensor_diff = sensors_after[min_index] - min_sensor
        t_other_sens_diff = 0.0
        for i in xrange(len(sensors_before)):
            if i != min_index:
                t_other_sens_diff += sensors_after[i] - sensors_before[i]        
        
        av_other_sens_diff = t_other_sens_diff/(len(sensors_after) - 1.0)



        fit = (av_other_sens_diff + min_sensor_diff)/2.0
        print "FITNESS of this GENOME: ", fit 
        return fit


    def eval_fitness(self,genomes):
        for g in genomes:
            while not self.on:
                #case when we dont want to be evaluating the genomes 
                sleep(5)
            
            start_sensors  = self.sensor_values
            net = nn.create_fast_feedforward_phenotype(g)
            self.current_nn = net

           # while start_sensors == None:
            #    print self.sensor_values
            #    start_sensors  = self.sensor_values  #this will be the current sensors from the robot
                #sleep(5)
            print "start sensor_values:", self.sensor_values
            print "NEat sleeping"
            sleep(20)
            print "done sleeping"
            print "FINISH sensor_values:", self.sensor_values

            finish_sensors = self.sensor_values
            g.fitness = self.fit_func(start_sensors,finish_sensors) 

    def run(self):
        local_dir = os.path.dirname(__file__)
        config = Config(os.path.join(local_dir, 'evolve_config'))

        pop = population.Population(config)
        pop.epoch(self.eval_fitness, 300)


        winner = pop.most_fit_genomes[-1]
        
        self.current_nn = winner

        print 'Number of evaluations: %d' % winner.ID
      
        # Verify network output against training data.
        print '\nBest network output:'
        net = nn.create_fast_feedforward_phenotype(winner)




if  __name__ == '__main__':
    
    anns = neat()
    anns.run()
