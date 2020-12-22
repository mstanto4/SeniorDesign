import numpy as np

class Measure:
	def __init__(self, num_notes, note_array):
		self.num_notes = num_notes

		# Numpy array of arrays of bools.
		self.notes = note_array

# Maybe determine number of measures beforehand and initialize list with
# that many values. This could avoid pointer issues.
measure_array = []

with open("test.sm", "r") as sm_file:
	lines = sm_file.readlines()

	# Detect start of notes
	for i in range(len(lines)):
		if lines[i].strip() == "#NOTES:":
			notes_start = i + 6
			break

curr_note = notes_start
measure_end = notes_start + 4

# Use tile function to easily initialize array of right form. Determine 
# values based on file content.
new_measure = Measure(4, np.tile(False, (4, 5)))

measure_array.append(new_measure)

print(new_measure.num_notes)
print(new_measure.notes)
