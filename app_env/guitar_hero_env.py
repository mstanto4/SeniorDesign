import gym
import json
import numpy as np

class GuitarHeroEnv(gym.Env):

	params = { "track_length": 1000,
		"note_speed": 10,	# Track units per step
		"bpm": 120,
		"perfect_threshold": 1,
		"great_threshold": 5,
		"okay_threshold": 8
	}


	def __init__(self, params_file=None, song_file="default"):

		if params_file != None:

			with open(params_file) as file:
				params = json.load(file)

		""" Code will go here that will load song_file and set parameters, etc.
		    accordingly. We'll decide what that looks like once we've 
		    pinned down a file format."""

		self.track_length = self.params["track_length"]
		self.bpm = self.params["note_speed"]
		self.bpm = self.params["bpm"]
		self.perfect_threshold = self.params["perfect_threshold"]
		self.great_threshold = self.params["great_threshold"]
		self.okay_threshold = self.params["okay_threshold"]
		# self.max_threshold = 10 --> set the max number of misses
		# possibly make max number of misses dependent on the level of difficulty the user is playing at 
		
	def step(self, action): 
		# need to define misses and time 
		
		# done = bool(
			# misses > self.max_threshold 
			# or time > self.track_length
		# )
		
		# if not done:
		
gh = GuitarHeroEnv()
