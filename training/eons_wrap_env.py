""" The purpose of this module is to enclose a rhythm game environment object 
    and scale the outputs so as to be more favorable with EONS."""

import sys
sys.path.append('../app_env')
from rhythm_game_env import *
from gym import spaces
import numpy as np

class EONSWrapperEnv:

	def __init__(self, params_file=None, song_file="test.smm", diff="Easy", net_efficacy=1):
		self.net_efficacy = net_efficacy
		self.rhythm_game_env = RhythmGameEnv(params_file, song_file, diff)
		#self.observation_space = spaces.Box(low=np.array([False for x in range(6)], dtype=bool), high=np.array([True for x in range(6)], dtype=bool))
		#self.action_space = spaces.Box(low=np.array([False for x in range(5)], dtype=bool), high=np.array([True for x in range(5)], dtype=bool))
		self.observation_space = spaces.Box(low=np.array([0.0, 0.0]), high=np.array([1.0, 1.0]))
		self.action_space = spaces.Discrete(2)
		self.prev_note = 0

	def step(self, action):
		assert (action in self.action_space), ""

		"""int_act = 0

		for i in range(5):
			int_act += 2 ** i * int(action[i])

		state, reward, done, info = self.rhythm_game_env.step(int_act)
		conv_state = np.array([False for x in range(6)], dtype=bool)

		bit_str = '{0:05b}'.format(state[0])

		for i in range(5):
			conv_state[i] = bool(bit_str[i])

		conv_state[5] = 0"""
		note = 0

		if action == 1:
			note = self.prev_note

		state, reward, done, info = self.rhythm_game_env.step(note)
		self.prev_note = state[0]
		state[0] /= 31.0

		if self.net_efficacy == 1:

			if state[1] <= self.rhythm_game_env.okay_threshold:
				state[-1] = 1.0

		elif self.net_efficacy == 2:

			if state[1] <= self.rhythm_game_env.great_threshold:
				state[-1] = 1.0

		else:

			if state[1] <= self.rhythm_game_env.perfect_threshold:
				state[-1] = 1.0

		if state[-1] != 1.0:
			state[-1] = 0

		assert (state in self.observation_space), "State must be array of six bools."

		return state, reward, done, info


	def seed(self, seed):
		pass

	
	def reset(self):
		self.rhythm_game_env.reset()
		return np.array([0.0, 0.0])

	
	def close(self):
		pass
