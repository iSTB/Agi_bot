from sound import sample
import time
import random




class player(object):

    def __init__(self):

        self.sounds = {}
        self.nn_state = {}
        self.last_played = {}
        self.refactory = 10
        self.threshold = 0.0 


    def update_state(self,nn):
        self.nn_state = nn

    def play(self):
        # print self.nn_state
        for key in self.nn_state:
            if self.nn_state[key] >= self.threshold:
                try:
                    self.play_sample(key)
                except:
                    print "Music player: dont have a sound:", key                    

    def add_sound(self,id,path):
        sound = sample(path)        
        self.sounds[id] = sound
        self.last_played[id] = time.time() - self.refactory

    def play_sample(self,id):

        if abs(time.time()-self.last_played[id]) > self.refactory:

            self.sounds[id].play()
            self.last_played[id] = time.time()
   


def make_random_nn():
    ann = {}
    for i in range(7):
        ann[i] = random.random()

    return ann


if __name__=="__main__":
    p = player()


    p.add_sound(0,'Sounds/BIO/01 - B.mp3')
    p.add_sound(1,'Sounds/BIO/02 - B.mp3')
    p.add_sound(2,'Sounds/BIO/03 - B.mp3')
    p.add_sound(3,'Sounds/BIO/04 - B.mp3')
    p.add_sound(4,'Sounds/MECH/01 - M.mp3')
    p.add_sound(5,'Sounds/MECH/02 - M.mp3')
    p.add_sound(6,'Sounds/MECH/03 - M.mp3')



    while True:

        p.update_state(make_random_nn())
        p.play()
        
        time.sleep(0.5)



