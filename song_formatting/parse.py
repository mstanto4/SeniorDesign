import sys

print(sys.argv[1])

#open .sm file to be read in and open new output .smm file
songData = open(sys.argv[1], 'r')
temp = sys.argv[1]
temp = temp + 'm'
newSong = open(temp, 'w+')

songContents = songData.readlines()

flag = 0
for count,x in enumerate(songContents):
	#save important information at the top 
	if(x[0] == '#'):
		text = x.split(':')
		if(text[0] == "#BANNER" or text[0] == "#BACKGROUND" or text[0] == "#MUSIC" or text[0] == "#OFFSET"):
			newSong.write(x)		
		if(text[0] == "#SAMPLESTART" or text[0] == "#SAMPLELENGTH" or text[0] == "#BPMS"):
			newSong.write(x)
		if(text[0] == "#TITLE" or text[0] == "#STOPS" or text[0] == "#DISPLAYBPM"):
			newSong.write(x)
		if(text[0] == "#NOTES"):
			newSong.write(x)
			newSong.write(songContents[count + 3])
	#copy over empty lines
	elif(x == '\n'):
		newSong.write(x)
	#copy over comments
	elif(x[0] == '/' and x[1] == '/'):
		newSong.write(x)
	#logic for inserting notes into the fifth column
	elif(x[0] == '0' or x[0] == '1' or x[0] == '2' or x[0] == '3' or x[0] == '4'):
		ones = 0
		for index, y in enumerate(x):
			if(y == '1'):
				ones = ones + 1
			#replace 2,3,4 with 1 because we do not want special notes
			if(y == '2' or y == '3' or y == '4'):
				temp = list(x)
				temp[index] = '1'
				x = ''.join(temp)
				ones = ones + 1
				flag = 1
		if(flag == 1 and ones < 2):
			temp = list(x)
			temp[4] = '1'
			x = ''.join(temp)
			x = x + '\n'
			flag = 0
		else:
			temp = list(x)
			temp[4] = '0'
			x = ''.join(temp)
			x = x + '\n'
		newSong.write(x)
	elif(x[0] == ','):
		newSong.write(x)
