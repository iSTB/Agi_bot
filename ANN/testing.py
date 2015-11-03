import numpy as np
import matplotlib.pyplot as plt
from esn import ESN
from tools import read_dataset, make_train_set,sig
import sys
def train(idxs, padIdxs, esn, stepper, inputs, outputs):
	all_states = []
	all_this = []
	for i, pv in enumerate(zip(padIdxs,idxs)):
		pad, val = pv
		
		print "with pad, from: ",pad[0]," to ",pad[1]
		state, output, this = stepper(
			inputs[pad[0]:pad[1],:], outputs[pad[0]:pad[1],:], 0.)
		# plot_state.extend(state[:,:units])
		# plot_output.extend(output)
		

		print "with val, from: ",val[0]," to ",val[1]
		for _ in xrange(10):
			state, output, this = stepper(
			inputs[val[0]:val[1],:], outputs[val[0]:val[1],:], 1.)

		# plot_state.extend(state[:,:units])
		# plot_output.extend(outputs[val[0]:val[1],:])

		##apply washout
		state = state[inital_washout:]
		this = this[inital_washout:]
		
		all_states.extend(state)
		all_this.extend(this)
		# import pdb;pdb.set_trace()
		err = np.mean((outputs[val[0]:val[1]-1,:] - output)**2,0)
		# err_sum +=err
		
		# print len(plot_output)

	# M_tonos = np.linalg.pinv(all_states)
	# import pdb; pdb.set_trace()
	# all_this = np.arctanh(all_this)
	# W_trans = np.dot(M_tonos,all_this)
	# esn.W_out.set_value(W_trans)
	# print W_trans
	
		# print err_sum
	return err

def test(sys, weight_scale, weight_inp, weight_fb, alpha, inital_washout, padding_s ):

	units = 28*28
	indim = 6
	outdim = 5
	# weight_scale = 1.
	# weight_inp = .4
	# weight_fb = .00001
	# alpha = .2
	# fback = True#False
	# inital_washout = 120#80
	# padding_s = 100

	esn = ESN(
		units, indim, outdim, weight_scale,weight_inp,weight_fb, alpha, fback
		)

	stepper = esn.step_taped()
	# runner = esn.run()
	# w_update = esn.update_weights()
	##data
	# steps = 300
	# zeros = np.zeros((steps,indim))
	# lnspace = np.linspace(-np.pi, np.pi, 100, False)
	# lnspace = np.tile(lnspace, steps/100)
	# zeros[:,0] = .5*np.sin(lnspace)
	# inputs = np.append(zeros, np.zeros(200)).reshape(500,1)
	# inputs = np.append(inputs,np.random.random((steps,indim))).reshape((2*steps,indim))
	
	dtsets = read_dataset(sys.argv[1], sys.argv[2])
	inputs, _, idxs, padIdxs = make_train_set(
		dtsets[1:], 0, 0, padding_s #[dtsets[0],dtsets[2]]
		)
	
	outputs = np.zeros((idxs[-1][1],outdim))-.5
	for i, n in enumerate(idxs):
		# outputs[n[0]:n[1],0] = (i%5)/5.
		# if n != idxs[-1]:
		outputs[n[0]:n[1],((i)%5)] = .5
	# import pdb;pdb.set_trace()
	plot_output =[]
	plot_state =[]

	import time
	start = time.time()
	###########TRAIN
	train(idxs, padIdxs, esn, stepper, inputs, outputs)
	###########END TRAIN
	print "Time taken ", time.time() - start
	#########TESTING#############
	# outputs = np.zeros((idxs[-1],1))
	inputs, _, idxs, padIdxs = make_train_set(
		dtsets, 0, 0, padding_s
		)
	
	outputs = np.zeros((idxs[-1][1],outdim)) 
	for i, n in enumerate(idxs):
		# outputs[n[0]:n[1],0] = (i%5)/5.
		outputs[n[0]:n[1],((i)%5)] = .6

	state, output, this = stepper(
		inputs, outputs, 0.)

	
	plot_state.extend(state[:,:units])
	plot_output.extend(output)

	success = np.zeros(output.shape[1])
	length = np.zeros(output.shape[1])
	for i_l,i_id in enumerate(idxs):
		length[(i_l%5)] += i_id[1] - i_id[0]
	for i_op, op in enumerate(output):
		for i_el, el in enumerate(zip(idxs,padIdxs)):
			if i_op in range(el[0][0],el[0][1]):
				if np.argmax(op) == (i_el%5):
					success[(i_el%5)] +=1
	print "Success: ",success, length
	print "Success %: ", success/length
		# np.append(output, outputs[:-2]).reshape(
		# outputs.shape[0],outputs.shape[1]+output.shape[1]))
	print len(plot_output)
	# import pdb;pdb.set_trace()
	#########TESTING#############

	
	if int(sys.argv[3]) == 1:
		f, axarr = plt.subplots(3, sharex=True)
		axarr[0].plot(plot_output,label="output")
		axarr[0].set_title('output')
		# axarr[0].legend()
		axarr[1].plot(plot_state,label="state")
		axarr[1].set_title('state')
		# axarr[1].legend()
		axarr[2].plot(inputs,label="inputs")
		axarr[2].set_title('inputs')
		# axarr[2].legend()
		# plt.draw()
		plt.show()
	
	return success/length



if __name__=="__main__":

	weight_scale = 1.#.8
	weight_inp = .2
	weight_fb = 10**(-3)
	alpha = .99#.35#.2
	fback = False#False
	inital_washout = 100#100
	padding_s = 300
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