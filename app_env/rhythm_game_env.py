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
		"note_speed": 4,	# Track units per step.
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
		self.curr_beat = 0
		
		self.curr_measure = 0
		self.curr_num_notes = measure_list[self.curr_measure].num_notes
		self.curr_note = 0

		self.visible_notes = []
		self.visible_note_distances = []

		# self.max_threshold = 10 --> set the max number of misses
		# possibly make max number of misses dependent on the level of difficulty the user is playing at 

		
	def step(self, action): 
		# need to define misses and time 
		
		# done = bool(
			# misses > self.max_threshold 
			# or time > self.track_length
		# )

		for i in range(len(self.visible_note_distances)):
			self.visible_note_distances[i] -= self.note_speed
		
		# Release a note when appropriate. Measure divided into 192 steps, so release every 192 / n steps.
		if self.num_steps % (192 / self.curr_num_notes) == 0:
			self.visible_notes.append(measure_list[self.curr_measure].notes[self.curr_note])
			self.visible_note_distances.append(self.track_length)
			self.curr_note += 1

		# Delete notes that are no longer visible.
		if self.visible_note_distances[0] < 0:
			del self.visible_notes[0]
			del self.visible_note_distances[0]

		self.num_steps += 1

		# Track beats for BPM changes and stops.
		if self.num_steps % (192 / 4) == 0:
			self.curr_beat += 1

		# Got to next measure and reset notes.
		if self.num_steps > 191:
			self.num_steps = 0
			
			"""TODO: Ensure that script can still step without errors once measures have 
			   been exhauseted. End condition should be empty visible_note list."""

			self.curr_measure += 1

			self.curr_note = 0

		print(self.visible_notes[0], self.visible_note_distances[0])

		
rg = RhythmGameEnv()

while True:
	rg.step(np.tile(False, (1, 5)))