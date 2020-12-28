import gym
import json
import numpy as np

class Measure:

	def __init__(self, num_notes, note_array):
		self.num_notes = num_notes

		# Numpy array of arrays of bools.
		self.notes = note_array


# Create a list of measures for testing step function
measure_list = []
measure_list.append(Measure(4, np.tile(True, (4, 5))))

measure2_notes = np.tile(False, (8, 5))

for i in range(5):
	measure2_notes[i][i] = True

measure_list.append(Measure(8, measure2_notes))


class RhythmGameEnv(gym.Env):

	params = { "track_length": 192,
		"note_speed": 1,	# Track units per step.
		"perfect_threshold": 5,
		"great_threshold": 10,
		"okay_threshold": 15
	}

	def __init__(self, params_file=None, song_file="default.txt"):

		if params_file != None:

			with open(params_file) as file:
				params = json.load(file)

		""" Code will go here that will load song_file and set parameters, etc.
		    accordingly. We'll decide what that looks like once we've 
		    pinned down a file format. Song file will set BPM(s)"""

		# This won't work until we narrow down a file format, just writing what it may look like.
		with open(song_file, "r") as file:
			self.notes = file.readlines()[12:]

		self.track_length = self.params["track_length"]
		self.note_speed = self.params["note_speed"]
		self.perfect_threshold = self.params["perfect_threshold"]
		self.great_threshold = self.params["great_threshold"]
		self.okay_threshold = self.params["okay_threshold"]
		self.dt = float(1 / 192)
		self.num_steps = 0
		
		self.curr_measure = 0
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

		
rg = RhythmGameEnv()
