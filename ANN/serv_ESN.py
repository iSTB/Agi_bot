import numpy as np
import matplotlib.pyplot as plt
from esn import ESN
from tools import read_dataset, make_train_set,sig
import sys
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

class serv_ESN():
	def __init__(self,):
		weight_scale = 1.#.8
		weight_inp = .2
		weight_fb = 10**(-3)
		alpha = .99#.35#.2
		fback = False#False
		inital_washout = 100#100
		padding_s = 300
		units = 28*28
		indim = 6
		outdim = 5

		self.esn = ESN(
			units, indim, outdim, weight_scale,weight_inp,weight_fb, alpha, fback
			)
		
		# self.webapp = webapp
		
		self.stepper = self.esn.step_taped()
		self.outputs = np.zeros((3,outdim))
		print "ESN:: init"
	def serv_close(self,):
		return True

	def serv_train(self,):
		return True

	def serv_step(self, val_in):
		
		state, output, this = self.stepper(
		val_in, self.outputs, 0.)

		return state, output, this


	#do what

	#send to whom

