from sound import sample





class player(object):

    def __init__(self):

        self.sounds = {}




    def add_sound(self,id,path):
        sound = sample(path)
        
        self.sounds[id] = sound




    def play(self,id):

        self.sounds[id].play()
   




p = player()


p.add_sound('1','Sounds/01 - B.mp3')
p.add_sound('2','Sounds/02 - B.mp3')
p.add_sound('3','Sounds/03 - B.mp3')
p.add_sound('4','Sounds/04 - B.mp3')
p.add_sound('5','Sounds/01 - M.mp3')
p.add_sound('6','Sounds/02 - M.mp3')
p.add_sound('7','Sounds/03 - M.mp3')


p.play('1')
p.play('2')
p.play('3')
p.play('4')
p.play('5')
p.play('6')
p.play('7')

