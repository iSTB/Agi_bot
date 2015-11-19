import numpy as np
import theano 
import theano.tensor as TT
from theano.tensor.shared_randomstreams import RandomStreams
import sys
import theano.sparse as sp
import scipy

np.random.seed(0xbeef)
rng = RandomStreams(seed=np.random.randint(1 << 30))
# theano.config.warn.subtensor_merge_bug = False

class ESN():
	def __init__(self,N,K,L,scale,scaleI,scaleFb,alpha,fback = False):
		self.units = N
		self.in_dim = K
		self.out_dim = L
		self.weight_scale = scale

		self.state_z = theano.shared(np.zeros(self.units+self.in_dim+self.out_dim).astype(theano.config.floatX))
		self.v_n = theano.shared(0.01*np.random.random(self.units))

		self.input = TT.matrix(name="inputs")
		self.d = TT.matrix(name="teacher")
		self.output = TT.matrix(name="outputs")
		self.coef = TT.scalar()

		self.W_in = theano.shared(
				scaleI*(
					scipy.sparse.rand(
							self.in_dim, self.units, density=.9)
				).todense().astype(theano.config.floatX)
				)

		W0 = self.weight_scale*(
				scipy.sparse.rand(
							self.units, self.units, density=.2)
				).todense()
		eigvals = np.linalg.eigvals(W0)
		lamda = np.max(np.absolute(eigvals))
		W1 = (1/np.absolute(lamda)) * W0
		self.W = theano.shared(
			(alpha * W1).astype(theano.config.floatX)
			)

		if fback:
			self.W_fb = theano.shared(
				scaleFb*(
					self.get_weights(
						size=(self.units,self.out_dim),low=-1., high=1.).astype(theano.config.floatX))
				)
		else:
			self.W_fb = theano.shared(
				self.weight_scale*( np.zeros((self.units,self.out_dim)).astype(theano.config.floatX))
				)

		self.W_out = theano.shared(
				self.weight_scale*(
					self.get_weights(
						size=(self.units+self.in_dim+self.out_dim,self.out_dim),\
						low=-1., high=1.).astype(theano.config.floatX))
				)

		self.M = TT.matrix()
		self.T = TT.matrix()
		self.f = TT.tanh

		def r(asd):
			return asd
		self.g = r


	def get_weights(self, size, low, high):
		return (high-low)*np.random.random(size)-high
		# return np.random.uniform(size=size, low= low, high=high)

	def step_taped(self,):
		def compute_state(u, t_tm1, state_tm1,  W, W_in, W_fb, W_out, c, randomn):
			#t-1
			term = TT.dot(state_tm1,W_out)
			#t-1
			y = self.g(term)
			#t-1
			x = state_tm1[:self.units]
			#t-1
			term1 = TT.dot(x, W)
			#t
			term2 = TT.dot(u, W_in)
			#t-1
			tmp = (c*t_tm1 + (1.-c)*y)
			term3 = TT.dot(W_fb, tmp)
			#t
			state_x = 0.0*state_tm1[:self.units] +\
			 self.f(term1+term2+term3+randomn)

			#t for statex, t-1 for u 
			state_tm1 = TT.set_subtensor(state_tm1[:self.units], state_x)
			#t for statex, t for u
			state_tm1 = TT.set_subtensor(state_tm1[self.units:(self.units+self.in_dim)], u)
			#t for output as well
			state_tm1 = TT.set_subtensor(state_tm1[(self.units+self.in_dim):], c*t_tm1 + (1.-c)*y )
			# state_tm1 = TT.set_subtensor(state_tm1[-self.out_dim:], y)
			# theano.printing.Print('this is a very important value')(state_tm1)
			return state_tm1, y, t_tm1

		# theano.printing.Print('this is a very important value')(self.state_z)
		#we have state_z and output for time scale T
		[state_z, output, dinv],_ = theano.scan(compute_state,
						sequences=[self.input, dict(input=self.d, taps=[-2])],
						outputs_info=[
							self.state_z, 
							None,
							None
							],
						non_sequences=[self.W, self.W_in, self.W_fb, self.W_out, self.coef, self.v_n]
			)

		#update state value for next iteration
		self.state_z = state_z
		self.output = output

		# a=theano.printing.Print("state_x")(self.state_z)
		# b=theano.printing.Print("output")(output)
		# c=theano.printing.Print("dinv")(dinv)
		return theano.function(inputs=[self.input, self.d, self.coef], outputs=[self.state_z, self.output, dinv])
	
	# def run(self,):

	# 	def compute_stateR(u, state_tm1,  W, W_in, W_fb, W_out):
	# 		#t-1
	# 		term = TT.dot(state_tm1,W_out)
	# 		#t-1
	# 		y = self.g(term)
	# 		#t-1
	# 		x = state_tm1[:self.units]
	# 		#t-1
	# 		term1 = TT.dot(x, W)
	# 		#t
	# 		term2 = TT.dot(u,W_in)
	# 		#t-1
	# 		term3 = TT.dot(W_fb, y)
	# 		#t
	# 		state_x = self.f(term1+term2+term3)
	# 		#t for statex, t-1 for u 
	# 		state_t = TT.set_subtensor(state_tm1[:self.units], state_x)
	# 		#t for statex, t for u
	# 		state_t = TT.set_subtensor(state_tm1[self.units:(self.units+self.in_dim)], u)
	# 		# state_tm1 = TT.set_subtensor(state_tm1[-self.out_dim:], y)
	# 		# theano.printing.Print('this is a very important value')(state_tm1)
	# 		return state_t, y

	# 	# theano.printing.Print('this is a very important value')(self.state_z)
	# 	#we have state_z and output for time scale T
	# 	[state_z, output],_ = theano.scan(compute_stateR,
	# 					sequences=[self.input],
	# 					outputs_info=[
	# 						self.state_z, 
	# 						None
	# 						],
	# 					non_sequences=[self.W, self.W_in, self.W_fb, self.W_out]
	# 		)

	# 	#update state value for next iteration
	# 	self.state_z = state_z
	# 	self.output = output

	# 	return theano.function(inputs=[self.input], outputs=[state_z, output])




