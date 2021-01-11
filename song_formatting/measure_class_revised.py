import numpy as np
import sys

class Measure:
        def __init__(self, num_notes, note_array):
                self.num_notes = num_notes

                # Numpy array of arrays of bools.
                self.notes = note_array

# Maybe determine number of measures beforehand and initialize list with
# that many values. This could avoid pointer issues.
easy_array = []
medium_array = []
hard_array = []
challenge_array = []

smm_file = open(sys.argv[1], "r")
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

for count, x in enumerate(lines):
	if(x[0] == '#'):
		text = x.strip()
		if(text == "#NOTES:"):
			text2 = lines[count+1].strip()
			print(text2)
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
			print(difficulty)
	
	elif(x[0] == ','):
		if(difficulty[len(difficulty)-1] == 1):
			easyMeasures.append(count)
		if(difficulty[len(difficulty)-1] == 2):
			mediumMeasures.append(count)
		if(difficulty[len(difficulty)-1] == 3):
			hardMeasures.append(count)
		if(difficulty[len(difficulty)-1] == 4):
			challengeMeasures.append(count)

for i in range(len(difficulty)):
	if(difficulty[i] == 1):
		for j in range(len(easyMeasures)):
			if(j == 0):
				numNotes = easyMeasures[j] - locNotes[i]
				print(numNotes)
	if(difficulty[i] == 2):
		for j in range(len(mediumMeasures)):
			if(j == 0):
				numNotes = mediumMeasures[j] - locNotes[i]
				print(numNotes)

	if(difficulty[i] == 3):
		for j in range(len(hardMeasures)):
			if(j == 0):
				numNotes = hardMeasures[j] - locNotes[i]
				print(numNotes)
		
	if(difficulty[i] == 4):		
		for j in range(len(challengeMeasures)):
			if(j == 0):
				numNotes = challengeMeasures[j] - locNotes[i]
				print(numNotes)




