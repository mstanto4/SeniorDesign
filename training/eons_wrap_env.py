""" The purpose of this module is to enclose a rhythm game environment object 
    and scale the outputs so as to be more favorable with EONS."""

import sys
sys.path.append('../app_env')
from rhythm_game_env import *
from gym import spaces
import numpy as np

class EONSWrapperEnv:

	def __init__(self, params_file=None, song_file="test.smm", diff="Easy"):
		self.rhythm_game_env = RhythmGameEnv(params_file, song_file, diff)
		self.observation_space = spaces.Box(low=np.array([0.0]), high=np.array([1.0]))
		self.action_space = spaces.Discrete(2)
		self.prev_note = 0

	def step(self, action):
		assert (action in self.action_space), "Action must be 0 or 1."

		note = 0

		if action == 1:
			note = self.prev_note

		state, reward, done, info = self.rhythm_game_env.step(note)
		# Stash note for later use
		self.prev_note = state[0]
		state[-1] /= self.rhythm_game_env.track_length

		assert (state[-1:] in self.observation_space), "State must be between 0 and 1."

		return state[-1:], reward, done, info


	def seed(self, seed):
		pass

	
	def reset(self):
		self.rhythm_game_env.reset()
		return np.array([0.0])

	
	def close(self):
		pass
