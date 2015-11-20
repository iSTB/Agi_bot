import numpy as np
import matplotlib.pyplot as plt
from esn import ESN
from tools import read_dataset, make_train_set,sig,createPad
import sys
def train(idxs, padIdxs, esn, stepper, inputs, outputs):
	all_states = []
	all_this = []
	err_sum = 0
	for i, pv in enumerate(zip(padIdxs,idxs)):
		pad, val = pv
		
		randompad = 0.01*createPad(200, 5)

		state, output, this = stepper(
				randompad, randompad, 0.)
		
		if (pad[1]-pad[0])!=0:
			print "with pad, from: ",pad[0]," to ",pad[1]
			state, output, this = stepper(
				inputs[pad[0]:pad[1],:], outputs[pad[0]:pad[1],:], .3)
		all_states.extend(state)
		all_this.extend(this)
		
		randompad = createPad(200, 5)

		state, output, this = stepper(
				randompad, randompad, 0.)
		
		print "with val, from: ",val[0]," to ",val[1]
		# for _ in xrange(10):
		state, output, this = stepper(
			inputs[val[0]:val[1],:], outputs[val[0]:val[1],:], 1.)
		##apply washout
		state = state[inital_washout:]
		this = this[inital_washout:]
		
		all_states.extend(state)
		all_this.extend(this)
		# import pdb;pdb.set_trace()
		err = np.mean((outputs[val[0]:val[1]-2,:] - output)**2,0)
		err_sum +=err.sum()
		
		# print len(plot_output)
	# plt.figure()
	# plt.plot(all_states)
	# plt.plot(all_this)
	# plt.show()

	print err_sum
	
		# print err_sum
	return all_states, all_this

def test(sys, weight_scale, weight_inp, weight_fb, alpha, inital_washout, padding_s ):

	units = 28*28
	indim = 6
	outdim = 6
	

	esn = ESN(
		units, indim, outdim, weight_scale,weight_inp,weight_fb, alpha, fback
		)
	esn.load("trainied.pickle")
	stepper = esn.step_taped()
	

	dtsets = read_dataset(sys.argv[1], sys.argv[2])
	# import pdb;pdb.set_trace()
	inputs, outputs, padIdxs, idxs = dtsets[0]

	
	plot_output =[]
	plot_state =[]

	import time
	start = time.time()
	###########TRAIN
	# all_states = []
	# all_this = []
	# all_states, all_this= train(idxs, padIdxs, esn, stepper, inputs, outputs)

	# M_tonos = np.linalg.pinv(all_states)
	# # import pdb; pdb.set_trace()
	# all_this = np.arctanh(all_this)
	# W_trans = np.dot(M_tonos,all_this)
	# esn.W_out.set_value(W_trans)
	# print W_trans
	
	###########END TRAIN
	print "Time taken ", time.time() - start
	#########TESTING#############
	
	outputs1 = np.zeros(outputs.shape)
	outputs1[1:] = outputs[:-1]

	state, output, this = stepper(
		inputs, outputs, 0.)

	print output.shape
	plot_state.extend(state[:,:units])
	plot_output.extend(output)

	
	#########TESTING#############
	if int(sys.argv[3]) == 1:
		f, axarr = plt.subplots(4, sharex=True)
		for oid,tpt in enumerate(np.array(plot_output).transpose()):
			try:
				axarr[0].plot(tpt,label="output"+str(oid))
			except:
				pass
		axarr[0].set_title('output')
		# axarr[0].legend()
		axarr[1].plot(outputs,label="outputs")
		axarr[2].plot(plot_state,label="state")
		axarr[2].set_title('state')
		# axarr[1].legend()
		axarr[3].plot(inputs,label="inputs")
		axarr[3].set_title('inputs')
		# axarr[2].legend()
		# plt.draw()
		# plt.figure()
		# plt.plot(inputs)
		# # plt.figure()
		# plt.plot(outputs)
		plt.show()
	
	# esn.save("trainied.pickle")

def save( filename, esn):
	import pickle
	f= open(filename, "wb")

	pickle.dump(esn, f, protocol=pickle.HIGHEST_PROTOCOL)
	f.close()

def load( filename):
	import pickle
	f=open(filename,"rb")
	esn = pickle.load(f)
	f.close()
	return esn


if __name__=="__main__":

	weight_scale = .8#.8
	weight_inp = 1.
	weight_fb = 1.#10**(-2)
	alpha = .450#.35#.2
	fback = True#False
	inital_washout = 10#100
	padding_s = 10#300
	stats = test(
		sys, weight_scale, weight_inp, weight_fb,
		 alpha, inital_washout, padding_s )
	


# weight_scale = 1.
	# weight_inp = .6
	# weight_fb = .00001
	# alpha = .1#.35#.2
	# fback = False#False
	# inital_washout = 100#100
	# padding_s = 300
	# #[ 0.82518797  0.82628062  0.6018471   0.72611139  0.90523416]
	












	# plt.figure()
	# plt.plot(plot_output,label="output")
	# plt.legend()
	# plt.figure()
	# plt.plot(plot_state,label="state")
	# plt.legend()
	# plt.figure()
	# plt.plot(inputs,label="inputs")
	# plt.legend()
	# plt.show()

	# for i, pv in enumerate(zip(padIdxs,idxs)):
	# 	pad, val = pv
		
	# 	print "with pad, from: ",pad[0]," to ",pad[1]
	# 	state, output, this,_,_,_ = stepper(
	# 		inputs[pad[0]:pad[1],:], outputs[pad[0]:pad[1],:], 0.)
	# 	plot_state.extend(state[:,:units])
	# 	plot_output.extend(output)
		
	# 	print "with val, from: ",val[0]," to ",val[1]
	# 	state, output, this,_,_,_ = stepper(
	# 		inputs[val[0]:val[1],:], outputs[val[0]:val[1],:], 0.)
	# 	plot_state.extend(state[:,:units])
	# 	plot_output.extend(output)
	# print inputs
	# print state.shape
	# print output