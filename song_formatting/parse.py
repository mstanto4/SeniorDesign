import sys

print(sys.argv[1])

songData = open(sys.argv[1], 'r')
temp = sys.argv[1]
temp = temp + 'm'
newSong = open(temp, 'w+')

songContents = songData.readlines()

print(songContents)

for x in songContents:
	if(x[0] == '#'):
		text = x.split(':')
		if(text[0] == "#BANNER" or text[0] == "#BACKGROUND" or text[0] == "#MUSIC" or text[0] == "#OFFSET"):
			newSong.write(x)		
		if(text[0] == "#SAMPLESTART" or text[0] == "#SAMPLELENGTH" or text[0] == "#BPMS" or text[0] == "#NOTES"):
			newSong.write(x)
	elif(x == '\n'):
		newSong.write(x)	
	elif(x[0] == '/' and x[1] == '/'):
		newSong.write(x)

