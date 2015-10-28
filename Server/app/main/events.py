from flask import session
from flask.ext.socketio import emit, join_room, leave_room
from .. import socketio
from Agi_bot.ANN import *
from Agi_bot.Sampler import *
from Agi_bot.XBEE import *

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def left(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

@socketio.on('start', namespace='/')
def start(message):
    #start all the apps: Music, Sampler, XBEE
    #hold references to session
    pass

@socketio.on('joined', namespace='/music')
def music_joined(message):
    '''
    Show Music related information
    join_room
    '''
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the music room.'}, room=room)

    

@socketio.on('joined', namespace='/ann')
def music_joined(message):
    '''
    Show ANN related information
    join_room
    '''
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the ANN room.'}, room=room)

    