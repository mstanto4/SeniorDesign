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

		self.dt = 1.0 / 60
		self.num_steps = 0
		self.measure_steps = 0
		self.curr_beat = 0
		self.curr_bpm = 120
		
		self.curr_measure = 0
		self.curr_num_notes = measure_list[self.curr_measure].num_notes
		self.curr_note = 0
		# self.curr_release_interval = 240 / (self.curr_bpm * self.curr_num_notes * self.dt)
		self.curr_note_spacing = self.note_speed * 240 / (self.curr_bpm * self.curr_num_notes * self.dt)

		self.visible_notes = []
		self.visible_note_distances = []

		self.score = 0

		# self.max_threshold = 10 --> set the max number of misses
		# possibly make max number of misses dependent on the level of difficulty the user is playing at 

		
	def step(self, action): 
		# need to define misses and time 
		
		# done = bool(
			# misses > self.max_threshold 
			# or time > self.track_length
		# )

		done = False

		# PSEUDOCODE 
		# if button press/action correctly corresponds to the next visible note
		
		# determine if button press/action is equla to the next visible note 
		equal = True 
		
		for i in self.visible_notes:
			if self.visible_notes[i] != action[i]:
				equal = False
		# if they are equal, determine point increase based on distance and threshold 
		if equal == True: 
			# falls under perfect threshold, add 3 points
			if self.visible_note_distances[0] < self.perfect_threshold:
				self.score += 3
			# falls under great threshold, add 2 points
			elif self.visible_note_distances[0] < self.great_threshold: 
				self.score += 2
			# falls under okay threshold, add 1 point
			elif self.visible_note_distances[0] < self.okay_threshold: 
				self.score += 1
			# miss, deduct 1 point 
			else:
				self.score -= 1
		# player missed/no action, deduct point 
		else:
			self.score -= 1


		for i in range(len(self.visible_note_distances)):
			self.visible_note_distances[i] -= self.note_speed

		# Delete notes that are no longer visible.
		if len(self.visible_notes) != 0 and self.visible_note_distances[0] < 0:
			del self.visible_notes[0]
			del self.visible_note_distances[0]

		# Environment run ends when no more notes are visible and all measures have been exhausted.
		if len(self.visible_notes) == 0 and self.curr_measure >= len(measure_list):
			done = True

		# Track beats for BPM changes and stops.
		self.curr_beat = int(self.num_steps * self.dt * self.curr_bpm / 60)

		note_pos = self.track_length + (self.curr_note_spacing * self.curr_note) - (self.note_speed * self.measure_steps)

		self.num_steps += 1
		self.measure_steps += 1

		if note_pos <= self.track_length:

			# Add note and current position if visible on track.
			if self.curr_measure < len(measure_list):
				self.visible_notes.append(measure_list[self.curr_measure].notes[self.curr_note])
				self.visible_note_distances.append(note_pos)
				self.curr_note += 1

			# Determine if measure exhausted. Reset params.
			if self.curr_note >= self.curr_num_notes:
				self.curr_measure += 1
				self.curr_note = 0
				self.measure_steps = 0

			if self.curr_measure < len(measure_list):
				self.curr_num_notes = measure_list[self.curr_measure].num_notes
				self.curr_note_spacing = self.note_speed * 240 / (self.curr_bpm * self.curr_num_notes * self.dt)

		return done

		
rg = RhythmGameEnv()
result = False

while not result:
	result = rg.step(np.tile(False, (1, 5)))

	if len(rg.visible_notes) != 0:
		print(rg.visible_notes[0], rg.visible_note_distances[0], rg.curr_note_spacing, rg.num_steps, rg.curr_beat)

		#print(rg.visible_note_distances)