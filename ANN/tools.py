import numpy as np
import os
import sys
import pickle
import theano
def sig(sig):
    return 1/(1+np.exp(-sig))

def _normalise(targets, yaw=0):
    print "Normalising values ", len(targets), len(targets[0])
    # normalise values
    maxes = []
    mins = []
    if yaw == 1:
        maxes = np.amax(targets, axis = 0)
        mins = np.amin(targets, axis = 0)

        for i, m in enumerate(zip(mins,maxes)):
            mi, ma = m
            if mi<0:
                targets[:,i] = ((targets[:,i]+abs(mi)))/(ma+abs(mi))
            else:
                targets[:,i] = ((targets[:,i]-abs(mi)))/(ma-abs(mi))
        targets = (targets*2.)-1.
        return targets 

    for t in targets:
        maxes.append(np.amax(t, axis = 0) )
        mins.append(np.amin(t, axis = 0) )
    
    maxes = np.amax(maxes, axis = 0)
    mins = np.amin(mins, axis = 0)

    targetss = []
    for t in targets:
        for i, m in enumerate(zip(mins,maxes)):
            mi, ma = m
            if mi<0:
                t[:,i] = ((t[:,i]+abs(mi)))/(ma+abs(mi))
            else:
                t[:,i] = ((t[:,i]-abs(mi)))/(ma-abs(mi))
        targetss.append(t)
    targets = targetss

    return targets    
def make_train_set(dataset, outc_size, pb_size, pad_size):
    '''
        returns 3 lists
        inputs: all the input series from all the movement sets, as ones
        bias: the paramteric bias trainig values
        outputs: creates the output targets for the input listss
    '''
    inputs = []
    bias = []
    outputs = []
    gestures_length = [0]
    pl = []
    gl = []
    for a_trial in dataset:
        # a_trial = _normalise(a_trial)
        for idx, gesture in enumerate(a_trial):
            pv = (gestures_length[-1],pad_size+gestures_length[-1])
            gestures_length.append(pad_size+gestures_length[-1])

            padding = []
            lnspace = np.linspace(np.pi, -np.pi, pad_size, False)
            for _ in xrange( len(gesture[1])):
                sign = 1. if np.random.random(1)>.5 else -1.
                padding.append(.5*sign*np.random.random(1)*np.sin(lnspace))
            padding = np.array(padding).transpose()
            # padding = padding.reshape(padding.shape[1],padding.shape[0])
            # padding = np.array(1.*np.random.random(
            #     (pad_size,len(gesture[1])) 
            #     )
            # )
            gestures_length.append(len(gesture)+gestures_length[-1])
            gv = (gestures_length[-1]-len(gesture),gestures_length[-1])
            # paddings.append(gestures_length[-1])
            # paddings.append(gestures_length[-1])
            pl.append(pv)
            gl.append(gv)
            # if pad_size != 0:
            #     padding = _normalise(padding, yaw=1)
            inputs.extend(padding.astype(theano.config.floatX))
            # gesture = gesture + 0.0001*np.random.random(gesture.shape)
            gesture = _normalise(gesture, yaw=1)
            # b = np.ones((gesture.shape[0],gesture.shape[1]+1))
            # b[:,:-1]=gesture
            # gesture = b
            inputs.extend(gesture.astype(theano.config.floatX))

            tmp_out = np.append(gesture[1:],gesture[0]).reshape(gesture.shape).astype(theano.config.floatX)
            # tmp_out = _normalise(tmp_out, yaw=1)
            outputs.extend(padding.astype(theano.config.floatX))
            outputs.extend(
                tmp_out
                )
            
            # pb = np.zeros(len(a_trial))
            # pb[idx] = 1.
            
            # parametric_bias = np.tile(pb, 
            #         gesture.shape[0]
            #         ).reshape(gesture.shape[0], len(a_trial)).astype(theano.config.floatX)
            # bias.extend(parametric_bias)

            #, np.array(bias)
    inputs = np.array(inputs)
    outputs = np.array(outputs)
    ##add bias##

    # inputs = _normalise(inputs, yaw=1)
    # outputs = _normalise(outputs, yaw=1)

    print gl, pl
    return np.array(inputs), np.array(outputs), gl, pl
def read_dataset(dirname, extension):

    returnables = []

    for file in os.listdir(dirname):
        if file.endswith("."+extension):
            print(file)
            script_dir = os.path.dirname(__file__)

            rel_path = dirname+"/"+file

            abs_file_path = os.path.join(script_dir, rel_path)
    
            f = open(abs_file_path, "rb")
            # read
            returnables.append(pickle.load(f))
            # save and close
            f.close()
    return returnables
