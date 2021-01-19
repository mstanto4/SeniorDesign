import numpy as np
import sys

class Measure:
        def __init__(self, num_notes, note_array):
                self.num_notes = num_notes

                # Numpy array of arrays of bools.
                self.notes = note_array

# Maybe determine number of measures beforehand and initialize list with
# that many values. This could avoid pointer issues.
#easy_array = []
#medium_array = []
#hard_array = []
#challenge_array = []

smm_file = open(sys.argv[1], "r")
lines = smm_file.readlines()

measure_array = []
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
	elif(x[0] == ','):
		if(difficulty[len(difficulty)-1] == "Easy"):
			easyMeasures.append(count)
		if(difficulty[len(difficulty)-1] == "Medium"):
			mediumMeasures.append(count)
		if(difficulty[len(difficulty)-1] == "Hard"):
			hardMeasures.append(count)
		if(difficulty[len(difficulty)-1] == "Challenge"):
			challengeMeasures.append(count)
if(not(sys.argv[2] in difficulty)):
	print("not valid difficulty")
	quit()
else:
	if(sys.argv[2] == "Easy"):
		measureList = easyMeasures
	elif(sys.argv[2] == "Medium"):
		measureList = mediumMeasures
	elif(sys.argv[2] == "Hard"):
		measureList = hardMeasures
	elif(sys.argv[2] == "Challenge"):
		measureList = challengeMeasures

position = difficulty.index(sys.argv[2]) 
for j in range(len(measureList)+1):
	if(j == 0):
		numNotes = measureList[j] - locNotes[position]
	elif(j == len(measureList) and (position+1) < len(locNotes)):
		numNotes = locNotes[position+1] - measureList[j-1] - 5
	elif(j == len(measureList)):
		numNotes = (len(lines) - 1) - measureList[j-1]
	else:
		numNotes = measureList[j] - measureList[j-1] - 1
	if(numNotes % 4 != 0):
		print(numNotes)
		print("Error")
		quit()
	new_measure = Measure(numNotes, np.tile(False, (numNotes, 5)))
	for k in range(0,numNotes):
		if(j == 0):
			temp = lines[locNotes[position]+k]
		else:
			temp = lines[measureList[j-1]+k+1]
		for m in range(0,5):
			if(temp[m] == '0'):
				new_measure.notes[k][m] = False
			else:
				new_measure.notes[k][m] = True 	
	measure_array.append(new_measure)
	print(new_measure.num_notes)
	print(new_measure.notes)	


#for i in range(len(difficulty)):
#	if(difficulty[i] == 1):
#		for j in range(len(easyMeasures)+1):
#			if(j == 0):
#				numNotes = easyMeasures[j] - locNotes[i]
#			elif(j == len(easyMeasures) and (i+1) < len(locNotes)):
#				numNotes = locNotes[i+1] - easyMeasures[j-1] - 5
#			elif(j == len(easyMeasures)):
#				numNotes = (len(lines) - 1) - easyMeasures[j-1]
#			else:
#				numNotes = easyMeasures[j] - easyMeasures[j-1] - 1
#			if(numNotes % 4 != 0):
#				print(numNotes)
#				print("Error")
#				quit()
#			new_measure = Measure(numNotes, np.tile(False, (numNotes, 5)))
#			for k in range(0,numNotes):
#				if(j == 0):
#					temp = lines[locNotes[i]+k]
#				else:
#					temp = lines[easyMeasures[j-1]+k+1]
#				for m in range(0,5):
#					if(temp[m] == '0'):
#						new_measure.notes[k][m] = False
#					else:
#						new_measure.notes[k][m] = True 	
#			easy_array.append(new_measure)
#	if(difficulty[i] == 2):
#		for j in range(len(mediumMeasures)+1):
#			if(j == 0):
#				numNotes = mediumMeasures[j] - locNotes[i]
#			elif(j == len(mediumMeasures) and (i+1) < len(locNotes)):
#				numNotes = locNotes[i+1] - mediumMeasures[j-1] - 5
#			elif(j == len(mediumMeasures)):
#				numNotes = (len(lines) - 1) - mediumMeasures[j-1]
#			else:
#				numNotes = mediumMeasures[j] - mediumMeasures[j-1] - 1
#			if(numNotes % 4 != 0):
#				print(numNotes)
#				print("Error")
#				quit()
#			new_measure = Measure(numNotes, np.tile(False, (numNotes, 5)))
#			for k in range(0,numNotes):
#				if(j == 0):
#					temp = lines[locNotes[i]+k]
#				else:
#					temp = lines[mediumMeasures[j-1]+k+1]
#				for m in range(0,5):
#					if(temp[m] == '0'):
#						new_measure.notes[k][m] = False
#					else:
#						new_measure.notes[k][m] = True 	
#			medium_array.append(new_measure)
#	if(difficulty[i] == 3):
#		for j in range(len(hardMeasures)+1):
#			if(j == 0):
#				numNotes = hardMeasures[j] - locNotes[i]
#			elif(j == len(hardMeasures) and (i+1) < len(locNotes)):
#				numNotes = locNotes[i+1] - hardMeasures[j-1] - 5
#			elif(j == len(hardMeasures)):
#				numNotes = (len(lines) - 1) - hardMeasures[j-1]
#			else:
#				numNotes = hardMeasures[j] - hardMeasures[j-1] - 1
#			if(numNotes % 4 != 0):
#				print(numNotes)
#				print("Error")
#				quit()
#			new_measure = Measure(numNotes, np.tile(False, (numNotes, 5)))
#			for k in range(0,numNotes):
#				if(j == 0):
#					temp = lines[locNotes[i]+k]
#				else:
#					temp = lines[hardMeasures[j-1]+k+1]
#				for m in range(0,5):
#					if(temp[m] == '0'):
#						new_measure.notes[k][m] = False
#					else:
#						new_measure.notes[k][m] = True 	
#			hard_array.append(new_measure)
#	if(difficulty[i] == 4):		
#		for j in range(len(challengeMeasures)+1):
#			if(j == 0):
#				numNotes = challengeMeasures[j] - locNotes[i]
#			elif(j == len(challengeMeasures) and (i+1) < len(locNotes)):
#				numNotes = locNotes[i+1] - challengeMeasures[j-1] - 5
#			elif(j == len(challengeMeasures)):
#				numNotes = (len(lines) - 1) - challengeMeasures[j-1]
#			else:
#				numNotes = challengeMeasures[j] - challengeMeasures[j-1] - 1
#			if(numNotes % 4 != 0):
#				print(numNotes)
#				print("Error")
#				quit()
#			new_measure = Measure(numNotes, np.tile(False, (numNotes, 5)))
#			for k in range(0,numNotes):
#				if(j == 0):
#					temp = lines[locNotes[i]+k]
#				else:
#					temp = lines[challengeMeasures[j-1]+k+1]
#				for m in range(0,5):
#					if(temp[m] == '0'):
#						new_measure.notes[k][m] = False
#					else:
#						new_measure.notes[k][m] = True	
#			challenge_array.append(new_measure)
