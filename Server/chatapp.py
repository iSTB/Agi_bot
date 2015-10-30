from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from datetime import datetime
import os
from Agi_bot.ANN import serv_ESN as ann


app = Flask(__name__)
app.config.from_pyfile('config.py')
ws = SocketIO(app)

last_messages = []


@app.route('/')
def hello_world():
    return render_template('index.html')

@ws.on('ann', namespace='/control')
def ann_contorl(data):
    #do something
    
    if data['data']:
        #switch off
        emit('notification', "ANN shutting down.",
         namespace='/control', broadcast=True)
    elif not data['data']:
        #switch on
        emit('notification', "ANN started.",
         namespace='/control', broadcast=True)

@ws.on('ann', namespace='/control_background')
def bg_ann_contorl(data):
    elif data['com']!= None and data['data']:
        #control switch board
        if data['com'] == "train":

            emit('notification', "ANN training.",
             namespace='/control', broadcast=True)
            
        elif data['com'] == "step":
            emit('notification', "ANN stepping.",
             namespace='/control', broadcast=True)
            

@ws.on('music', namespace='/control')
def ann_contorl(data):
    #do something
    
    if data['data']:
        #switch off
        emit('notification', "MUSIC shutting down.",
         namespace='/control', broadcast=True)
    else:
        #switch on
        emit('notification', "MUSIC started.",
         namespace='/control', broadcast=True)

@ws.on('xbee', namespace='/control')
def ann_contorl(data):
    #do something
    
    if data['data']:
        #switch off
        emit('notification', "XBEE shutting down.",
         namespace='/control', broadcast=True)
    else:
        #switch on
        emit('notification', "XBEE started.",
         namespace='/control', broadcast=True)
            

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3001))
    ws.run(app, host='0.0.0.0', port=port)
