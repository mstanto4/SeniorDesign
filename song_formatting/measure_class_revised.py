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
			easy_array.append(new_measure)
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
			medium_array.append(new_measure)
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
			hard_array.append(new_measure)
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
			challenge_array.append(new_measure)
