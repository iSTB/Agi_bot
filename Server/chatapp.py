#server
from gevent import monkey
monkey.patch_all()
# import subprocess
# subprocess._has_poll = False

import flask
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

#engine
from Agi_bot.ANN.serv_ESN import serv_ESN 
from Agi_bot.Sampler.player import player 
from Agi_bot.XBEE.XBee_Threaded import XBee 
from Agi_bot.neat.evole import neat as NEAT 
from Agi_bot.drawer.drawer import net_drawer
#os
from datetime import datetime
import os, sys
import numpy as np
from time import sleep,time
from threading import Thread
import subprocess



app = Flask(__name__)
app.config.from_pyfile('config.py')
ws = SocketIO(app)
# cs = SocketIO()
ann = None
xbee = None
status = [['a'],['b','r'],['c','s'],['d'],['e','l'],['f']]
xbee_motors_on = [['A'],['B'],['C','P'],['D'],['E'],['F']]
xbee_motors_off = [['a'],['b','r'],['c','s'],['d'],['e','l'],['f']]
thread = None
music = None
music_thread = None
ai = None
ai_thread = None
draw_weights = None
draw = None
echo_on = True
time_to_run = 60*60*3.4
ai_start = time() 

def check_time(mins = 10):
    global ai_start
    global echo_on
    global time_to_run
    if time() - ai_start >= time_to_run:
        # echo_on = not(echo_on)
        pass

    # if datetime.timedelta(minutes = 10) - 


@app.route('/')
def hello_world():
    return render_template('index.html')

##############################################FRONT
######################ANN
@ws.on('ann', namespace='/control')
def ann_contorl(data):
    #do something
    
    if data['data']:
        #switch off
        package = {
            "from":"front",
            "data":"close"}
        emit(
            'ann',
            package,
            namespace='/control_background',
            broadcast=True)
        emit('notification', "ANN shutting down.",
         namespace='/control', broadcast=True)
        print "ANN:: OFF"

    elif not data['data']:
        #switch on
        package = {
            "from":"front",
            "data":"init"}
        emit(
            'ann',
            package,
            namespace='/control_background',
            broadcast=True)        
        emit('notification', "ANN started.",
         namespace='/control', broadcast=True)
        print "ANN:: ON"
######################MUSIC
@ws.on('music', namespace='/control')
def music_contorl(data):
    #do something
    if data['data']:
        #switch off
        package = {
            "from":"front",
            "data":"close"
            }

        emit(
            'music',
            package,
            namespace='/control_background',
            broadcast=True
            )
        emit('notification', "MUSIC shutting down.",
         namespace='/control', broadcast=True)
        print "MUSIC:: OFF"
    else:
        #switch on
        package = {
            "from":"front",
            "data":"init"
            }

        emit(
            'music',
            package,
            namespace='/control_background',
            broadcast=True
            )
        emit('notification', "MUSIC started.",
         namespace='/control', broadcast=True)
        print "MUSIC:: ON"
######################XBEE
@ws.on('xbee', namespace='/control')
def xbee_contorl(data):
    #do something
    
    if data['data']:
        #switch off
        package = {
            "from":"front",
            "data":"close"
            }

        emit(
            'xbee',
            package,
            namespace='/control_background',
            broadcast=True
            )
        emit('notification', "XBEE shutting down.",
         namespace='/control', broadcast=True)
        print "XBEE:: OFF"
    else:
        #switch on
        package = {
            "from":"front",
            "data":"init"
            }

        emit(
            'xbee',
            package,
            namespace='/control_background',
            broadcast=True
            )
        emit('notification', "XBEE started.",
         namespace='/control', broadcast=True)
        print "XBEE:: ON"
######################################################################BACK
######################ANN
@ws.on('ann', namespace='/control_background')
def bg_ann_ctrl(socket_data):
    global ann
    global ai
    global ai_thread
    global draw
    global draw_weights
    global echo_on
    global time_to_run
    #from who
    if socket_data['from'] == "xbee":
        if socket_data['data'] != None and ann is not None:
            #received sennsors, norm between [0,1]
            check_time()
    
            normed = (np.array(socket_data['data']))/550.
            sen = (normed*2.)-1.
            state, output = ann.serv_step(sen)
            state = state.tolist()
            output = output.tolist()
            # print "SENSE:: ",list(normed[0])
            if echo_on:
                ai.turn_off()

            if not echo_on:
                print "NEAT ON!"
                ai.turn_on()
                print "giving these to neat:",list(normed[0])
                ai.set_sensors(list(normed[0]))
                output = [ai.get_motor(list(normed[0]))]
                print "NEAT OUT",output
            # print "WHY",len(state[0])#[:-612]
            
            draw.update(state[0][:-612])
                    
            package = {
                "from": "ann",
                "data": [state[0][50:175]]
                }
            emit(
                "music",
                package,
                namespace="/control_background")
            package = {
                "from": "ann",
                "data": output#motor_command#
                }
            emit(
                "xbee",
                package,
                namespace="/control_background")
            print "ANN:: xbee com"
        else:
            #invalid
            emit(
                "notification", 
                "Error in command received in XBEE by ::"+socket_data['from'], 
                namespace='/control', 
                broadcast=True
                )
            print "ANN:: xbee com error"
    elif socket_data['from'] == "music":
        if socket_data['data'] != None and ann is not None:
            print "music read in ANN"#, socket_data['data'] 
        else:
            #invalid
            emit(
                "notification", 
                "Error in command received in MUSIC by ::"+socket_data['from'], 
                namespace='/control', 
                broadcast=True
                )
            print "ANN:: music error"
        #recieve something musicy
    elif socket_data['from'] == "front":
        if socket_data['data'] == "init" and ann == None:
            ann = serv_ESN()
            draw_weights = np.asmatrix(np.asarray(ann.esn.W.get_value())[:-600,:-600])
            # print draw_weights
            draw = net_drawer(draw_weights)
            ai = NEAT()
            @flask.copy_current_request_context            
            def ai_thrd():
              #  while ai_thread is not None:
                ai.run()

                #sleep(0.5)
            if ai_thread is None:
                ai_thread = Thread(target=ai_thrd)
                ai_thread.start()

            print "ANN:: from front init"
        elif socket_data['data'] == "close" and ann != None:
            ann = None
            ai_thread.join(1)
            ai_thread = None
            ai = None
            draw.close()
            print "ANN:: from front close"
        else:
            # print socket_data
            emit(
                "notification", 
                "Error in ANN "+socket_data['data']+" from ::"+socket_data['from'], 
                namespace='/control', 
                broadcast=True
            ) 
            print "ANN:: from front error"  
    else:
        #invalid
        emit(
            "notification", 
            "Error in command received in ANN by ::"+socket_data['from'], 
            namespace='/control', 
            broadcast=True
            )
        print "ANN:: Generic error"
######################MUSIC
@ws.on('music', namespace='/control_background')
def bg_music_ctrl(socket_data):
    global music
    global music_thread


    if socket_data['from'] == "ann" and music is not None:
        state = {}
        for i, v in enumerate(socket_data['data'][0]):#[34:47]):
            state[i] = v
        #print state
        music.update_state(state)

        print "MUSIC:: from ann com "#, socket_data['data']
    elif socket_data['from'] == "xbee" and music is not None:
        pass
    elif socket_data['from'] == "music" and music is not None:
        pass
    elif socket_data['from'] == "front":
        if socket_data['data'] == "init" and music is None:
            music = player()
            # global music
            # cur_index = 0


            #bio_sounds = os.listdir('../Sampler/Sounds/BIO')
            conf_sounds = ['../Sampler/Sounds/DRONE SOUNDS/Confident/' + x for x in os.listdir('../Sampler/Sounds/DRONE SOUNDS/Confident')]
            rel_sounds = ['../Sampler/Sounds/DRONE SOUNDS/Relaxed/' + x for x in os.listdir('../Sampler/Sounds/DRONE SOUNDS/Relaxed')]
            fear_sounds = ['../Sampler/Sounds/DRONE SOUNDS/Fearful/' + x for x in os.listdir('../Sampler/Sounds/DRONE SOUNDS/Fearful')]
            all_sounds = conf_sounds +rel_sounds+fear_sounds

            for i,sound in enumerate(all_sounds):                
                music.add_sound(i,sound)
                
            @flask.copy_current_request_context            
            def m_thread():



                #music.add_sound(0,'../Sampler/Sounds/BIO/01 - B.mp3')
                #music.add_sound(1,'../Sampler/Sounds/BIO/02 - B.mp3')
                #music.add_sound(2,'../Sampler/Sounds/BIO/03 - B.mp3')
                #music.add_sound(3,'../Sampler/Sounds/BIO/04 - B.mp3')
                #music.add_sound(4,'../Sampler/Sounds/MECH/01 - M.mp3')
                #music.add_sound(5,'../Sampler/Sounds/MECH/02 - M.mp3')
                #music.add_sound(6,'../Sampler/Sounds/MECH/03 - M.mp3')
                #music.add_soun
                while music_thread is not None:
                    try:
                        music.play()
                    except Exception as e:
                        print "MUSIC excpetion ",e
                        break
                    sleep(2)

            if music_thread is None:
                music_thread = Thread(target=m_thread)
                music_thread.start()

            return True
        elif socket_data['data'] == "close" and music is not None:
            music = None
            music_thread.join(1)
            music_thread = None
            p = subprocess.Popen(['pkill','mpg123'])     

            return True
        else:
            emit(
                "notification", 
                "Error in MUSIC from ::"+socket_data['from'], 
                namespace='/control', 
                broadcast=True
            )    
    else:
        emit(
            "notification", 
            "Error in command received in MUSIC by ::"+socket_data['from'], 
            namespace='/control', 
            broadcast=True
            )
        print "MUSIC:: Generic error"
######################XBEE


@ws.on('xbee', namespace='/control_background')
def bg_xbee_ctrl(socket_data):
    global xbee
    global thread
    global status
    global xbee_motors_on
    global xbee_motors_off
    #from who
    if socket_data['from'] == "ann":
        if socket_data['data'] != None:
            #received sensors
            print "XBEE:: ann com"#, socket_data['data']
            #send data to the xbee
            if xbee is not None:
                print "NET OUT:: ",np.argmax(socket_data['data'][0])
                max_id = np.argmax(socket_data['data'][0])
                #check wahts on close it
                for i,v in enumerate(xbee_motors_on):
                    if v == status[i] and i != max_id:
                        status[i] = xbee_motors_off[i]
                        for val in status[i]:
                            xbee.SendStr(val)
                            # pass
                #turn max on 
                status[max_id] = xbee_motors_on[max_id]
                for val in status[max_id]:
                    xbee.SendStr(val)
                    # pass
                # for idx,value in enumerate(socket_data['data'][0]):
                #     print "\t motor val:", value, " |id:",idx," ", xbee_motors_on[idx]
                #     #only send when changed
                #     if value >= 0.0 and status[idx]!=xbee_motors_on[idx]:
                #         xbee.SendStr(xbee_motors_on[idx])
                #     elif value < 0.0 and status[idx]!=xbee_motors_off[idx]:
                #         xbee.SendStr(xbee_motors_off[idx])
                #     else:
                #         print "ANN:: Nothing to change"

        else:
            #invalid
            emit(
                "notification", 
                "XBEE::Error in command received by ::"+socket_data['from'], 
                namespace='/control', 
                broadcast=True
                )
            print "XBEE:: ann com error"
    elif socket_data['from'] == "music":
        if socket_data['data'] != None:
            print "XBEE:: music com"
        else:
            #invalid
            emit(
                "notification", 
                "XBEE::Error in command received by ::"+socket_data['from'], 
                namespace='/control', 
                broadcast=True
                )
            print "XBEE:: music com error"

        #recieve something musicy
    elif socket_data['from'] == "xbee":
        print "XBEE:: xbee com", socket_data['data'] 

        pass
    elif socket_data['from'] == "front":
        if socket_data['data'] == "init" and ann != None:
            # xbee = 1
            print "1"
            if xbee == None:
                xbee = XBee("/dev/ttyUSB0")
                # xbee = 1
            else:
                pass
                # return True
            print xbee
            #xbee.run()
            @flask.copy_current_request_context
            def xbee_thread():
                while (thread is not None):
                    # sleep(1)
                    #send msg
                    msg = None
                    # while msg is None:
                    try:
                        xbee.SendStr('0')
                        msg = xbee.Receive()
                        # msg = np.random.random(6).tolist()
                        print "MSG ",msg
                    except Exception as e:
                        print e
                        break
                    if msg:
                        if len(msg) == 1:
                            #we have a signle digit response
                            continue
                        package = {
                            "from":"xbee",
                            "data": [msg]
                            }

                        emit(
                            'ann',
                            package,
                            namespace='/control_background'
                            )
                    sleep(10)

            if thread is None:
                thread = Thread(target=xbee_thread)
                thread.start()
            print "XBEE:: front com init"
            return True
        elif socket_data['data'] == "close" and xbee != None:
            if thread is not None:
                thread.join(1)
                thread = None
            for _ in xrange(5):
                xbee.SendStr('1')
                xbee.SendStr('s')
                sleep(0.5)
            '''
            # xbee.shutdown()
            # xbee.stop()
            # xbee.join(2)
            # xbee = None        
            '''
            print "XBEE:: front com close"
            return True
        elif socket_data['data'] == "emit" and xbee != None:
            print "XBEE:: front com emit"
            return True
        else:
            # print socket_data
            emit(
                "notification", 
                "XBEE::Error "+socket_data['data']+" from ::"+socket_data['from']+"\n make sure ANN is ON", 
                namespace='/control', 
                broadcast=True
            )
            print "XBEE:: front com error"   
    else:
        #invalid
        emit(
            "notification", 
            "Error in command received in XBEE by ::"+socket_data['from'], 
            namespace='/control', 
            broadcast=True
            )
        print "XBEE:: Generic error"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3001))
    try:
        ws.run(app, host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        print "FORCE "
        thread.join(1)
        ai_thread.join(1)
        music_thread.join(1)
        xbee_thread.join(1)
        draw.close()
        sys.exit(1)
