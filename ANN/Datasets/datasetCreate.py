import numpy as np
import matplotlib.pyplot as plt


def createPad(size):
	padding = []
	lin_size = 20
	
	lnspace = np.linspace(np.pi, -lin_size*np.pi, size, False)
	for _ in xrange( 6):
		sign = 1. if np.random.random(1)>.5 else -1.
		padding.append(
			sign*np.random.random()*np.sin(lnspace)
			)

	padding = np.array(padding).transpose()
	return padding

def create_dtst():
	#make the random set
	inps = np.zeros((3000,6))
	# inps = a
	padding = createPad(200)
	inps[:200] = padding
	#make the fake 1+3 sensor ON, turn left
	sensor_noise = (((np.random.random((1300,4))*2)-1.)*.3) - .2
	sensor_active = np.random.random((500,4))*.2 + .75
	inps[200:1500,1] = sensor_noise[:,0]
	inps[200:1500,3:] = sensor_noise[:,1:]
	inps[200:700,0] = sensor_active[:,0]
	inps[200:700,2] = sensor_active[:,1]

	#make the fake 1+5 sensor ON, turn right
	padding = createPad(200)
	inps[1500:1700] = padding
	#make the fake 1+3 sensor ON, turn left
	sensor_noise = (((np.random.random((1300,4))*2)-1.)*.3) - .2
	sensor_active = np.random.random((500,4))*.2+.8
	inps[1700:,1:4] = sensor_noise[:,1:]
	inps[1700:,5] = sensor_noise[:,0]
	inps[1700:2200,0] = sensor_active[:,0]
	inps[1700:2200,4] = sensor_active[:,1]

	outs = np.zeros((3000,6))
	outs[200:700,1] = .9
	outs[200:700,5] = .9 
	outs[700:1500,2] = .9
	
	outs[1700:2200,0] = .9
	outs[1700:2200,4] = .9 
	outs[2200:,2] = .9
	

	plt.plot(outs)
	plt.figure()
	plt.plot(inps)
	plt.show()
	import pdb;pdb.set_trace()
	pading_idxs = [(0,200),(1500,1700)]
	val_idxs = [(200,1500),(1700,3000)]
	return inps, outs, pading_idxs, val_idxs

if __name__=="__main__":
	inps, outs, pading_idxs, val_idxs = create_dtst()
	import pickle
	f = open("taining_set.pickle","wb")
	pickle.dump([inps, outs, pading_idxs, val_idxs],f)
	f.close()


