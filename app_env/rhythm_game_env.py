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
		"note_speed": 4,	# Track units per step.
		"perfect_threshold": 5,
		"great_threshold": 10,
		"okay_threshold": 15
	}

	def __init__(self, params_file=None, song_file=sys.argv[1]):

		if params_file != None:

			with open(params_file) as file:
				params = json.load(file)

		# Maybe determine number of measures beforehand and initialize list with
		# that many values. This could avoid pointer issues.
		self.easy_array = []
		self.medium_array = []
		self.hard_array = []
		self.challenge_array = []

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
						difficulty.append(1)
						locNotes.append(count+2)
					if(text2 == "Medium:"):
						difficulty.append(2)
						locNotes.append(count+2)
					if(text2 == "Hard:"):
						difficulty.append(3)
						locNotes.append(count+2)
					if(text2 == "Challenge:"):
						difficulty.append(4)
						locNotes.append(count+2)
			
			elif(x[0] == ','):
				if(difficulty[len(difficulty)-1] == 1):
					easyMeasures.append(count)
				if(difficulty[len(difficulty)-1] == 2):
					mediumMeasures.append(count)
				if(difficulty[len(difficulty)-1] == 3):
					hardMeasures.append(count)
				if(difficulty[len(difficulty)-1] == 4):
					challengeMeasures.append(count)
		
		#sets up the measure array for each difficulty present in the file
		for i in range(len(difficulty)):
			if(difficulty[i] == 1):
				for j in range(len(easyMeasures)+1):
					if(j == 0):
						numNotes = easyMeasures[j] - locNotes[i]
					elif(j == len(easyMeasures) and (i+1) < len(locNotes)):
						numNotes = locNotes[i+1] - easyMeasures[j-1] - 5
					elif(j == len(easyMeasures)):
						numNotes = (len(lines) - 1) - easyMeasures[j-1]
					else:
						numNotes = easyMeasures[j] - easyMeasures[j-1] - 1
					if(numNotes % 4 != 0):
						print(numNotes)
						print("Error")
						quit()
					new_measure = Measure(numNotes, np.tile(False, (numNotes, 5)))
					for k in range(0,numNotes):
						if(j == 0):
							temp = lines[locNotes[i]+k]
						else:
							temp = lines[easyMeasures[j-1]+k+1]
						for m in range(0,5):
							if(temp[m] == '0'):
								new_measure.notes[k][m] = False
							else:
								new_measure.notes[k][m] = True 	
					self.easy_array.append(new_measure)
			if(difficulty[i] == 2):
				for j in range(len(mediumMeasures)+1):
					if(j == 0):
						numNotes = mediumMeasures[j] - locNotes[i]
					elif(j == len(mediumMeasures) and (i+1) < len(locNotes)):
						numNotes = locNotes[i+1] - mediumMeasures[j-1] - 5
					elif(j == len(mediumMeasures)):
						numNotes = (len(lines) - 1) - mediumMeasures[j-1]
					else:
						numNotes = mediumMeasures[j] - mediumMeasures[j-1] - 1
					if(numNotes % 4 != 0):
						print(numNotes)
						print("Error")
						quit()
					new_measure = Measure(numNotes, np.tile(False, (numNotes, 5)))
					for k in range(0,numNotes):
						if(j == 0):
							temp = lines[locNotes[i]+k]
						else:
							temp = lines[mediumMeasures[j-1]+k+1]
						for m in range(0,5):
							if(temp[m] == '0'):
								new_measure.notes[k][m] = False
							else:
								new_measure.notes[k][m] = True 	
					self.medium_array.append(new_measure)
			if(difficulty[i] == 3):
				for j in range(len(hardMeasures)+1):
					if(j == 0):
						numNotes = hardMeasures[j] - locNotes[i]
					elif(j == len(hardMeasures) and (i+1) < len(locNotes)):
						numNotes = locNotes[i+1] - hardMeasures[j-1] - 5
					elif(j == len(hardMeasures)):
						numNotes = (len(lines) - 1) - hardMeasures[j-1]
					else:
						numNotes = hardMeasures[j] - hardMeasures[j-1] - 1
					if(numNotes % 4 != 0):
						print(numNotes)
						print("Error")
						quit()
					new_measure = Measure(numNotes, np.tile(False, (numNotes, 5)))
					for k in range(0,numNotes):
						if(j == 0):
							temp = lines[locNotes[i]+k]
						else:
							temp = lines[hardMeasures[j-1]+k+1]
						for m in range(0,5):
							if(temp[m] == '0'):
								new_measure.notes[k][m] = False
							else:
								new_measure.notes[k][m] = True 	
					self.hard_array.append(new_measure)
			if(difficulty[i] == 4):		
				for j in range(len(challengeMeasures)+1):
					if(j == 0):
						numNotes = challengeMeasures[j] - locNotes[i]
					elif(j == len(challengeMeasures) and (i+1) < len(locNotes)):
						numNotes = locNotes[i+1] - challengeMeasures[j-1] - 5
					elif(j == len(challengeMeasures)):
						numNotes = (len(lines) - 1) - challengeMeasures[j-1]
					else:
						numNotes = challengeMeasures[j] - challengeMeasures[j-1] - 1
					if(numNotes % 4 != 0):
						print(numNotes)
						print("Error")
						quit()
					new_measure = Measure(numNotes, np.tile(False, (numNotes, 5)))
					for k in range(0,numNotes):
						if(j == 0):
							temp = lines[locNotes[i]+k]
						else:
							temp = lines[challengeMeasures[j-1]+k+1]
						for m in range(0,5):
							if(temp[m] == '0'):
								new_measure.notes[k][m] = False
							else:
								new_measure.notes[k][m] = True	
					self.challenge_array.append(new_measure)

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

		# self.max_threshold = 10 --> set the max number of misses
		# possibly make max number of misses dependent on the level of difficulty the user is playing at 

		
	def step(self, action): 
		done = False
		reward = 0

		# No notes, and input is given.
		if len(self.visible_notes) == 0:

			if action != [False for x in range(5)]:
				reward = -1

		# Note is within scoring range.
		elif self.visible_note_distances[0] <= self.okay_threshold:

			if self.visible_notes[0] == action:

				if self.visible_note_distances[0] <= self.perfect_threshold:
					reward = 3

				elif self.visible_note_distances[0] <= self.great_threshold: 
					reward = 2
				
				elif self.visible_note_distances[0] <= self.okay_threshold: 
					reward = 1

			else:
				reward = -1

		else:

			if action != [False for x in range(5)]:
				reward = -1


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

		# Track position of current note to determine when to make visible.
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

		if len(self.visible_notes == 0):
			state = [[False for x in range(5)], 0]

		else:
			state = [self.visible_notes[0], self.visible_note_distances[0]]



		return done, reward, state

		
rg = RhythmGameEnv()
result = False

while not result:
	result = rg.step(np.tile(False, (1, 5)))

	if len(rg.visible_notes) != 0:
		print(rg.visible_notes[0], rg.visible_note_distances[0], rg.curr_note_spacing, rg.num_steps, rg.curr_beat)

		#print(rg.visible_note_distances)
