from gevent import monkey
monkey.patch_all()

import flask
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from datetime import datetime
import os
from Agi_bot.ANN.serv_ESN import serv_ESN 
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
last_messages = []


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
        print "XBEE:: OFF"
######################################################################BACK
######################ANN
@ws.on('ann', namespace='/control_background')
def bg_ann_ctrl(socket_data):
    global ann
    #from who
    if socket_data['from'] == "xbee":
        if socket_data['data'] != None and ann is not None:
            #received sensors
            ann.serv_step(socket_data['data'])
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
            print "music read in ANN", socket_data['data'] 
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
######################XBEE


@ws.on('xbee', namespace='/control_background')
def bg_xbee_ctrl(socket_data):
    global xbee
    global thread
    #from who
    if socket_data['from'] == "ann":
        if socket_data['data'] != None:
            #received sensors
            print "XBEE:: ann com", socket_data['data'] 
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
            xbee = 1
            @flask.copy_current_request_context
            def xbee_thread():
                while thread is not None:
                    sleep(.01)
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
