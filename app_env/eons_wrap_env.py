""" The purpose of this module is to enclose a rhythm game environment object 
    and scale the outputs so as to be more favorable with EONS."""

import sys
sys.path.append('../neuro_lib')
import neuro
from rhythm_game_env import *
from gym import spaces
import numpy as np

class EONSWrapperEnv:

	def __init__(self, params_file=None, song_file="test.smm", diff="Easy", net_efficacy=1):
		self.rhythm_game_env = RhythmGameEnv(params_file, song_file, diff)
		self.observation_space = spaces.Box(low=np.array([0.0]), high=np.array([1.0]))
		self.net_efficacy = net_efficacy
		self.action_space = spaces.Discrete(2)
		self.saved_note = 0

	def step(self, action):
		assert (action in self.action_space), "Action must be 0 or 1."

		note = 0

		if action == 1:
			note = self.saved_note

		state, reward, done, info = self.rhythm_game_env.step(note)
		# Stash note for later use
		self.saved_note = state[0]
		wrapper_state = 0

		# Efficacy determines at what point network receives "play" signal.
		if self.net_efficacy == 1:

			if state[-1] <= self.rhythm_game_env.okay_threshold:
				wrapper_state = 1

		elif self.net_efficacy == 2:

			if state[-1] <= self.rhythm_game_env.great_threshold:
				wrapper_state = 1

		else:
			
			if state[-1] <= self.rhythm_game_env.perfect_threshold:
				wrapper_state = 1
			

		assert ([wrapper_state] in self.observation_space), "State must be between 0 and 1."

		return [wrapper_state], reward, done, info


	def seed(self, seed):
		pass

	
	def reset(self):
		self.rhythm_game_env.reset()
		return np.array([0])

	
	def close(self):
		pass
