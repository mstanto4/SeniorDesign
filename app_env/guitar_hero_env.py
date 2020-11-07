import gym
import json
import numpy as np

class GuitarHeroEnv(gym.Env):

	params = { "track_length": 100,
		"note_speed": 1,	# Track units per step.
		"perfect_threshold": 1,
		"great_threshold": 5,
		"okay_threshold": 8
	}


	def __init__(self, params_file=None, song_file="default.txt"):

		if params_file != None:

			with open(params_file) as file:
				params = json.load(file)

		""" Code will go here that will load song_file and set parameters, etc.
		    accordingly. We'll decide what that looks like once we've 
		    pinned down a file format. Song file will set BPM"""

		# This won't work until we narrow down a file format, just writing what it may look like.
		with open(song_file, "r") as file:
			self.notes = file.readlines()[12:]

		self.track_length = self.params["track_length"]
		self.note_speed = self.params["note_speed"]
		self.perfect_threshold = self.params["perfect_threshold"]
		self.great_threshold = self.params["great_threshold"]
		self.okay_threshold = self.params["okay_threshold"]

		# Store all note distances for easy updating. Once a distance is negative, 
		# it is no longer needed.
		self.note_distances = np.array([self.track_length + (i * 10) for i in range(len(self.notes))])

		# State consists of distance from closest note to end of track.
		self.state = [self.notes[0], self.note_distances[0]]
		self.curr_note = 0
		# self.max_threshold = 10 --> set the max number of misses
		# possibly make max number of misses dependent on the level of difficulty the user is playing at 

		
	def step(self, action): 
		# need to define misses and time 
		
		# done = bool(
			# misses > self.max_threshold 
			# or time > self.track_length
		# )
		
		# if not done:
		pass
		
gh = GuitarHeroEnv()
