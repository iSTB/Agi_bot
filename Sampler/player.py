from sound import sample
import time
import random
import numpy as np
import os


class player(object):

    def __init__(self):

        self.sounds = {}
        self.nn_state = {}
        self.act_av = 0.0 #stores average activation of nerurons
        self.act_std = 0.0 # stores the standard devarion of the activation neruons 
        self.last_played = {}
        self.refactory = 90
        self.threshold = 0.0 


    def update_state(self,nn):
        self.nn_state = nn
        self.av = np.average(self.nn_state.values())
        self.std = np.std(self.nn_state.values())
        self.threshold = self.av + self.std*(1.25)

        n_neurons = len(self.nn_state.values())
        n_sounds = len(self.sounds.values())
    
        if n_neurons > n_sounds: # case when we have more neurons than sounds
            for i in range(n_sounds,n_neurons):
                self.add_sound(i,self.sounds.values()[i % n_sounds].path)
    def play(self):
        # print self.nn_state
        for key in self.nn_state:
            if self.nn_state[key] >= self.threshold:
                #try:
                self.play_sample(key)
                #except:
                 #   print "Music player: dont have a sound:", key                    

        time.sleep(1.5)
    def add_sound(self,id,path):
        sound = sample(path)        
        self.sounds[id] = sound
        self.last_played[id] = time.time() - self.refactory

    def play_sample(self,id):

        if abs(time.time()-self.last_played[id]) > self.refactory:

            self.sounds[id].play()
            self.last_played[id] = time.time()
            #self.sleep(0.1) 


def make_random_nn(n):
    ann = {}
    for i in range(n):
        ann[i] = random.random()

    return ann


if __name__=="__main__":

    p = player()

    conf_path = './Sounds/DRONE SOUNDS/Confident'
    rel_path = './Sounds/DRONE SOUNDS/Relaxed'
    fear_path = './Sounds/DRONE SOUNDS/Fearful'

    conf_sounds = [conf_path + '/' + x for x in os.listdir(conf_path)]
    rel_sounds = [rel_path + '/' + x for x in os.listdir(rel_path)]
    fear_sounds = [fear_path + '/' + x for x in os.listdir(fear_path)]
    
    all_sounds = conf_sounds + rel_sounds + fear_sounds

    for i,sound in enumerate(all_sounds):
        p.add_sound(i,sound) 

    n_sounds = len(all_sounds)

    print "Number of sounds:", n_sounds    

    while True:

        p.update_state(make_random_nn(n_sounds+600))
        p.play()
        print p.sounds
        
        #time.sleep(1.5)



