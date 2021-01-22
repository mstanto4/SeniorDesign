import gym
import json
import numpy as np
import sys

class Measure:

	def __init__(self, num_notes, note_array):
		self.num_notes = num_notes

		# Numpy array of arrays of bools.
		self.notes = note_array

class RhythmGameEnv(gym.Env):

	params = { "track_length": 192,
		"note_speed": 1,	# Track units per step.
		"perfect_threshold": 5,
		"great_threshold": 10,
		"okay_threshold": 15
	}

	empty_note = [False for x in range(5)]

	def __init__(self, params_file=None, song_file="test.smm", diff="Easy"):

		if params_file != None:

			with open(params_file) as file:
				params = json.load(file)

		# Maybe determine number of measures beforehand and initialize list with
		# that many values. This could avoid pointer issues.
		self.measure_list = []
		self.bpms = []
		self.bpm_trans_points = []
		self.stops = {}

		smm_file = open(song_file, "r")
		lines = smm_file.readlines()

		#keep track of which lines the measures end at
		easyMeasures = []
		mediumMeasures = []
		hardMeasures = []
		challengeMeasures = []
		#determines which difficulty the current measure is located in
		difficulty = []
		#determines where the notes for each difficulty start
		locNotes = []
			
		#read in measures and determine the location of the end of each measure and which difficulties are present in the file
		for count, x in enumerate(lines):
			if(x[0] == '#'):
				text = x.strip()
				if(text == "#NOTES:"):
					text2 = lines[count+1].strip()
					if(text2 == "Easy:"):
						difficulty.append("Easy")
						locNotes.append(count+2)
					if(text2 == "Medium:"):
						difficulty.append("Medium")
						locNotes.append(count+2)
					if(text2 == "Hard:"):
						difficulty.append("Hard")
						locNotes.append(count+2)
					if(text2 == "Challenge:"):
						difficulty.append("Challenge")
						locNotes.append(count+2)
				text2 = x.strip().split(':')
				if(text2[0] == "#OFFSET"):
					self.offset = float(text2[1][:-1])
				# elif(text2[0] == "#SAMPLESTART"):
				#	self.sample_start = float(text2[1])
				# elif(text2[0] == "#SAMPLELENGTH"):
				#	self.sample_start = float(text2[1])

				elif(text2[0] == "#BPMS"):
					temp = text2[1].split(',')
					#remove ;
					temp[len(temp)-1] = temp[len(temp)-1][:-2]
					for i in range(len(temp)):
						bpm_pair = temp[i].split('=')
						# self.bpms[float(bpm_pair[0])] = float(bpm_pair[1])
						self.bpm_trans_points.append(float(bpm_pair[0]))
						self.bpms.append(float((bpm_pair[1])))
				elif(text2[0] == "#STOPS"):
					temp = text2[1].split(',')

					if len(temp) > 1:
						temp[len(temp)-1] = temp[len(temp)-1][:-2]

						for i in range(len(temp)):
							stop_pair = temp[i].split('=')
							self.stops[float(stop_pair[0])] = float(stop_pair[1])		
			elif(x[0] == ','):
				if(difficulty[len(difficulty)-1] == "Easy"):
					easyMeasures.append(count)
				if(difficulty[len(difficulty)-1] == "Medium"):
					mediumMeasures.append(count)
				if(difficulty[len(difficulty)-1] == "Hard"):
					hardMeasures.append(count)
				if(difficulty[len(difficulty)-1] == "Challenge"):
					challengeMeasures.append(count)

		#pick the correct set of measure locations for the difficulty
		if(diff not in difficulty):
			print("not valid difficulty")
			quit()
		else:
			if(diff == "Easy"):
				measureLocations = easyMeasures
			elif(diff == "Medium"):
				measureLocations = mediumMeasures
			elif(diff == "Hard"):
				measureLocations = hardMeasures
			elif(diff == "Challenge"):
				measureLocations = challengeMeasures		

		position = difficulty.index(diff)
		print("Commas detected:", len(measureLocations))
		for j in range(len(measureLocations)+1):
			if(j == 0):
				numNotes = measureLocations[j] - locNotes[position]
			elif(j == len(measureLocations) and (position+1) < len(locNotes)):
				numNotes = locNotes[position+1] - measureLocations[j-1] - 5
			elif(j == len(measureLocations)):
				numNotes = (len(lines) - 1) - measureLocations[j-1]
			else:
				numNotes = measureLocations[j] - measureLocations[j-1] - 1
			if(numNotes % 4 != 0):
				print(numNotes)
				print("Error")
				quit()
			new_measure = Measure(numNotes, np.tile(False, (numNotes, 5)))
			for k in range(0,numNotes):
				if(j == 0):
					temp = lines[locNotes[position]+k]
				else:
					temp = lines[measureLocations[j-1]+k+1]
				for m in range(0,5):
					if(temp[m] == '0'):
						new_measure.notes[k][m] = False
					else:
						new_measure.notes[k][m] = True
			self.measure_list.append(new_measure)

		self.track_length = self.params["track_length"]
		self.note_speed = self.params["note_speed"]
		self.perfect_threshold = self.params["perfect_threshold"]
		self.great_threshold = self.params["great_threshold"]
		self.okay_threshold = self.params["okay_threshold"]

		self.dt = 1.0 / 60
		self.num_steps = 0
		self.measure_steps = 0
		self.curr_beat = 0
		self.curr_bpm = self.bpms[0]
		
		self.curr_measure = 0
		self.curr_num_notes = self.measure_list[self.curr_measure].num_notes
		self.curr_note = 0
		# self.curr_release_interval = 240 / (self.curr_bpm * self.curr_num_notes * self.dt)
		self.curr_note_spacing = self.note_speed * 240 / (self.curr_bpm * self.curr_num_notes * self.dt)

		self.visible_notes = []
		self.visible_note_distances = []

		# self.max_threshold = 10 --> set the max number of misses
		# possibly make max number of misses dependent on the level of difficulty the user is playing at 

		
	def step(self, action): 
		done = False
		reward = 0

		# No notes, and input is given.
		if len(self.visible_notes) == 0:

			if action != self.empty_note:
				reward = -1

		# Note is within scoring range.
		elif self.visible_note_distances[0] <= self.okay_threshold:

			if list(self.visible_notes[0]) == self.empty_note:
				reward = 0

			elif list(self.visible_notes[0]) == action:

				if self.visible_note_distances[0] <= self.perfect_threshold:
					reward = 3

				elif self.visible_note_distances[0] <= self.great_threshold: 
					reward = 2
				
				elif self.visible_note_distances[0] <= self.okay_threshold: 
					reward = 1

			else:
				reward = -1

			if reward != 0:
				del self.visible_notes[0]
				del self.visible_note_distances[0]

		else:

			if action != self.empty_note:
				reward = -1


		for i in range(len(self.visible_note_distances)):
			self.visible_note_distances[i] -= self.note_speed

		# Delete notes that are no longer visible.
		if len(self.visible_notes) != 0 and self.visible_note_distances[0] < 0:
			del self.visible_notes[0]
			del self.visible_note_distances[0]

		# Environment run ends when no more notes are visible and all measures have been exhausted.
		if len(self.visible_notes) == 0 and self.curr_measure >= len(self.measure_list):
			done = True

		if done:
			return done, reward, [self.empty_note, 0]

		# Track beats for BPM changes and stops.
		self.curr_beat = self.calc_beat(self.num_steps)

		
		if self.curr_beat in self.bpm_trans_points:
			self.curr_bpm = self.bpms[self.bpm_trans_points.index(self.curr_beat)]

		# Track position of current note to determine when to make visible.
		note_pos = self.track_length + (self.curr_note_spacing * self.curr_note) - (self.note_speed * self.measure_steps)

		self.num_steps += 1
		self.measure_steps += 1

		if note_pos <= self.track_length:

			# Add note and current position if visible on track.
			if self.curr_measure < len(self.measure_list) and self.curr_note < self.curr_num_notes:
				self.visible_notes.append(self.measure_list[self.curr_measure].notes[self.curr_note])
				self.visible_note_distances.append(note_pos)
				self.curr_note += 1

			# Determine if measure exhausted. Reset params.
			if self.curr_note >= self.curr_num_notes and self.curr_beat % 4 == 0:
				self.curr_measure += 1
				self.curr_note = 0
				self.measure_steps = 0

			if self.curr_measure < len(self.measure_list):
				self.curr_num_notes = self.measure_list[self.curr_measure].num_notes
				self.curr_note_spacing = self.note_speed * 240 / (self.curr_bpm * self.curr_num_notes * self.dt)

		if len(self.visible_notes) == 0:
			state = [self.empty_note, 0]

		else:
			state = [self.visible_notes[0], self.visible_note_distances[0]]



		return done, reward, state


	def calc_beat(self, curr_step):
		prebeat = self.num_steps * self.dt * self.curr_bpm / 60.00

		return int(prebeat)

		
