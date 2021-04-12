import gym
from gym import spaces
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
		"perfect_threshold": 10,
		"great_threshold": 15,
		"okay_threshold": 30
	}

	empty_note = [False for x in range(5)]

	def __init__(self, params_file=None, song_file="test.smm", diff="Easy"):

		if params_file != None:

			with open(params_file) as file:
				params = json.load(file)

		self.measure_list = []
		self.bpms = []
		self.bpm_beats = []
		self.stop_beats = []
		self.stop_durs = []

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

				elif(text2[0] == "#BPMS"):
					temp = text2[1].split(',')
					temp[len(temp)-1] = temp[len(temp)-1][:-1]
					for i in range(len(temp)):
						bpm_pair = temp[i].split('=')
						self.bpm_beats.append(float(bpm_pair[0]))
						self.bpms.append(float((bpm_pair[1])))
				elif(text2[0] == "#STOPS"):
					temp = text2[1].split(',')

					if len(temp) > 1:
						temp[len(temp)-1] = temp[len(temp)-1][:-1]

						for i in range(len(temp)):
							stop_pair = temp[i].split('=')
							self.stop_beats.append(float(stop_pair[0]))
							self.stop_durs.append(float(stop_pair[1]) * 60.0)

				elif(text2[0] == "#TITLE"):
					self.title = text2[1]
					self.title = self.title[:-1]
				elif(text2[0] == "#MUSIC"):
					self.music = text2[1]
					self.music = self.music[:-1]
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
		self.bpm_steps = [0]
		self.stop_steps = []

		for i in range(1, len(self.bpm_beats)):
			self.bpm_steps.append(0)

			for j in range(i):
				self.bpm_steps[i] += int((self.bpm_beats[j + 1] - self.bpm_beats[j]) * 60.0 / (self.bpms[j] * self.dt))

		for i in range(len(self.stop_beats)):
			self.stop_steps.append(0)
			remains = self.stop_beats[i]

			for j in range(len(self.bpm_beats)):

				if self.stop_beats[i] >= self.bpm_beats[j]:
					self.stop_steps[i] = self.bpm_steps[j]

				else:
					# Convert remaining beats to steps.
					self.stop_steps[i] += ((self.stop_beats[i] - self.bpm_beats[j - 1]) / self.bpms[j - 1]) * 60 / self.dt
					self.stop_steps[i] = int(self.stop_steps[i])

					# Introduce delay to future bpm changes.
					for k in range(len(self.bpm_steps)):

						if self.bpm_steps[k] > self.stop_steps[i]:
							self.bpm_steps[k] += self.stop_durs[i]
		
		self.curr_measure = 0
		self.curr_num_notes = self.measure_list[self.curr_measure].num_notes
		self.curr_note = 0
		# Spacing as a function of bpm and dt (frame rate). Spacing is variable; 
		# note speed is constant to make transistions between measures easier.
		self.curr_note_spacing = self.note_speed * 240 / (self.curr_bpm * self.curr_num_notes * self.dt)

		self.visible_notes = []
		self.visible_note_distances = []

		self.action_space = spaces.Box(low=np.array([0]), high=np.array([31]))
		self.observation_space = spaces.Box(low=np.array([0.0, 0.0]), high=np.array([31.0, self.track_length]))

		
	def step(self, action): 
		"""Progress the state of the game by dt seconds. React to given action.
		   Return reward, resultant state, and whether or not the game is done."""

		assert (np.array([action]) in self.action_space), "Action must be an integer between 0 and 31." 

		# Convert integer action to boolean list.
		action_array = []
		i = 5
		d = 16

		while i >= 1:
			action_array.append(bool(int(action) & int(d)))
			d /= 2
			i -= 1

		done = False
		stopped = False
		reward = 0
		info = None

		# No notes, and input is given.
		if len(self.visible_notes) == 0:

			if action_array != self.empty_note:
				reward = -1

		# Note is within scoring range.
		elif self.visible_note_distances[0] <= self.okay_threshold:

			if action_array == self.empty_note:
				reward = 0

				if self.visible_note_distances[0] < self.note_speed and list(self.visible_notes[0]) != list(self.empty_note):
					#print("note slipped")
					reward = -1

			elif list(self.visible_notes[0]) == action_array:

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

		# Note outside of scoring range.
		else:

			if action_array != self.empty_note:
				reward = -1

		# Bring visible notes closer to the end area.
		for i in range(len(self.visible_note_distances)):
			self.visible_note_distances[i] -= self.note_speed

		# Delete notes that are no longer visible.
		while len(self.visible_notes) != 0 and self.visible_note_distances[0] < 0:
			del self.visible_notes[0]
			del self.visible_note_distances[0]

		# Environment run ends when no more notes are visible and all measures have been exhausted.
		if len(self.visible_notes) == 0 and self.curr_measure >= len(self.measure_list):
			done = True

		if done:
			return [0, 0], reward, done, info

		# Track beats for BPM changes and stops.
		self.curr_beat = self.calc_beat(self.num_steps)

		if self.num_steps in self.bpm_steps:
			self.curr_bpm = self.bpms[self.bpm_steps.index(self.num_steps)]

		# Check if steps in stop interval.
		for i in range(len(self.stop_steps)):

			if self.num_steps >= self.stop_steps[i] and self.num_steps <= self.stop_steps[i] + self.stop_durs[i]:
				stopped = True
				break

		# increment steps and return state
		if stopped:
			self.num_steps += 1

			if len(self.visible_notes) == 0:
				state = [0, 0]

			else:
				state = [list_to_5bit(self.visible_notes[0]), self.visible_note_distances[0]]

			assert (np.array(state) in self.observation_space), "Invalid ovservation."
			return state, reward, done, info


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
			state = [0, 0]

		else:

			"""int_state = 0;
			s = 4

			for bit in self.visible_notes[0]:
				int_state += int(bit) << s
				s -= 1"""

			state = [list_to_5bit(self.visible_notes[0]), self.visible_note_distances[0]]
			assert (np.array(state) in self.observation_space), "Invalid ovservation."

		return state, reward, done, info

	
	def reset(self):
		self.__init__()
		return np.array([0, 0])


	def calc_beat(self, curr_step):
		"""Determine on which beat a step will occur. Useful for converting 
		   BPM change and stop locations."""
		
		beat_calc = curr_step * self.dt * self.curr_bpm / 60.0

		# Stitch beats together like a piecewise function.
		for i in range(1, len(self.bpm_steps)):

			if curr_step >= self.bpm_steps[i]:

				beat_calc += self.dt * self.bpm_steps[i] * (self.bpms[i - 1] - self.bpms[i]) / 60.0

		return int(beat_calc)

	
def list_to_5bit(bools):
	new_int = 0
	s = 4

	for bit in bools:
		new_int += int(bit) << s
		s -= 1

	return new_int
