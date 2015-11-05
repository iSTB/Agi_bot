#server
from gevent import monkey
monkey.patch_all()

import flask
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

#engine
# from Agi_bot.ANN.serv_ESN import serv_ESN 
from Agi_bot.Sampler.player import player 
from Agi_bot.XBEE.XBee_Threaded import XBee 
#os
from datetime import datetime
import os
import numpy as np
from time import sleep
from threading import Thread



app = Flask(__name__)
app.config.from_pyfile('config.py')
ws = SocketIO(app)
# cs = SocketIO()
ann = None
xbee = None
thread = None
music = None
music_thread = None


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
    #from who
    if socket_data['from'] == "xbee":
        if socket_data['data'] != None and ann is not None:
            #received sensors
            state, output = ann.serv_step(socket_data['data'])
            state = state.tolist()
            output = output.tolist()
            package = {
                "from": "ann",
                "data": state
                }
            emit(
                "music",
                package,
                namespace="/control_background")
            package = {
                "from": "ann",
                "data": output
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
            print "ANN:: from front init"
        elif socket_data['data'] == "close" and ann != None:
            ann = None
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
        for i, v in enumerate(socket_data['data'][0][34:47]):
            state[i%6] = v
        print state
        music.update_state(state)
        print "MUSIC:: from ann com "#, socket_data['data']
    elif socket_data['from'] == "xbee" and music is not None:
        pass
    elif socket_data['from'] == "music" and music is not None:
        pass
    elif socket_data['from'] == "front":
        if socket_data['data'] == "init" and music is None:
            music = player()
            @flask.copy_current_request_context            
            def m_thread():
                global music
                music.add_sound(0,'../Sampler/Sounds/BIO/01 - B.mp3')
                music.add_sound(1,'../Sampler/Sounds/BIO/02 - B.mp3')
                music.add_sound(2,'../Sampler/Sounds/BIO/03 - B.mp3')
                music.add_sound(3,'../Sampler/Sounds/BIO/04 - B.mp3')
                music.add_sound(4,'../Sampler/Sounds/MECH/01 - M.mp3')
                music.add_sound(5,'../Sampler/Sounds/MECH/02 - M.mp3')
                music.add_sound(6,'../Sampler/Sounds/MECH/03 - M.mp3')

                while music_thread is not None:
                    try:
                        music.play()
                    except Exception:
                        break
                    sleep(1)

            if music_thread is None:
                music_thread = Thread(target=m_thread)
                music_thread.start()

            return True
        elif socket_data['data'] == "close" and music is not None:
            music = None
            music_thread.join(1)
            music_thread = None
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
    #from who
    if socket_data['from'] == "ann":
        if socket_data['data'] != None:
            #received sensors
            print "XBEE:: ann com"#, socket_data['data']

            #send data to the xbee
            if xbee is not None:
                xbee.Send(
                    bytearray.fromhex("7e 7d 11 13 5b 01 01 01 01 01 01 01"))

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
        if socket_data['data'] == "init" and xbee == None and ann != None:
            # xbee = 1
            xbee = XBee("COM3")
            @flask.copy_current_request_context
            def xbee_thread():
                while thread is not None:
                    sleep(1)
                    #send msg
                    msg = xbee.Receive()
                    if msg:
                        content = msg[7:-1]
                        print xbee.format(content)
                        package = {
                            "from":"xbee",
                            "data": np.random.random((3,6)).tolist()
                            }

                        emit(
                            'ann',
                            package,
                            namespace='/control_background'
                            )

            if thread is None:
                thread = Thread(target=xbee_thread)
                thread.start()
            print "XBEE:: front com init"
            return True
        elif socket_data['data'] == "close" and xbee != None:
            xbee.shutdown()
            xbee = None        
            thread.join(1)
            thread = None
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
    ws.run(app, host='0.0.0.0', port=port)
