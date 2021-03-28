#for including gym / probably wont need or will need to change on pi
import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')
sys.path.append('../firmware')

cheese0 = 175
cheese1 = 315
cheese2 = 450
cheese3 = 580
cheese4 = 725

#import button_func as bf
import rhythm_game_env
import numpy as np
import pyglet as pyg
from pyglet.window import key
from pyglet import font

class GameState():
	def __init__(self):	
		self.done = False
		self.score = 0
		self.reward = 0
		self.state = []
		self.blank_note = [False for x in range(5)]
		self.action = self.blank_note
		self.rows_visible = []	

	def update(self, dt):
	#	print(keys)
	#	print(self.action)
		#button stuff
	#	self.action = bf.read_button()
	#	if(self.action[0] == True):
	#		press[0] = 1;
	#	else:
	#		press[0] = 0;
	#	if(self.action[1] == True):
	#		press[1] = 1;
	#	else:
	#		press[1] = 0;
	#	if(self.action[2] == True):
	#		press[2] = 1;
	#	else:
	#		press[2] = 0;
	#	if(self.action[3] == True):
	#		press[3] = 1;
	#	else:
	#		press[3] = 0;
	#	if(self.action[4] == True):
	#		press[4] = 1;
	#	else:
	#		press[4] = 0;


		self.done, self.reward, self.state = rg.step(self.action)
		self.score += self.reward
		if(self.reward != 0):
			print(self.score)
		self.action = [False for x in range(5)]
		
		if(len(notes1) != 0):
			for x in range(0, len(notes1)):
				del notes1[0];
		if(len(notes2) != 0):
			for x in range(0, len(notes2)):
				del notes2[0];
		if(len(notes3) != 0):
			for x in range(0, len(notes3)):
				del notes3[0];
		if(len(notes4) != 0):
			for x in range(0, len(notes4)):
				del notes4[0];
		if(len(notes5) != 0):
			for x in range(0, len(notes5)):
				del notes5[0];

		for num, note in enumerate(rg.visible_notes):
			if(note[0] == True):
				notes1.append(pyg.sprite.Sprite(note_image, x = cheese0, y = 350 - 1.7*(192 - rg.visible_note_distances[num]), batch=note_batch))
			if(note[1] == True):
				notes2.append(pyg.sprite.Sprite(note_image, x = cheese1, y = 350 - 1.7*(192 - rg.visible_note_distances[num]), batch=note_batch))
			if(note[2] == True):
				notes3.append(pyg.sprite.Sprite(note_image, x = cheese2, y = 350 - 1.7*(192 - rg.visible_note_distances[num]), batch=note_batch))
			if(note[3] == True):
				notes4.append(pyg.sprite.Sprite(note_image, x = cheese3, y = 350 - 1.7*(192 - rg.visible_note_distances[num]), batch=note_batch))
			if(note[4] == True):
				notes5.append(pyg.sprite.Sprite(note_image, x = cheese4, y = 350 - 1.7*(192 - rg.visible_note_distances[num]), batch=note_batch))


		
#		score = pyg.text.Label(text="Score:" + str(self.score), color = (255,255,255,255), font_name = haster, x = 1250, y = 550)	

	#	print(rg.visible_notes)
	#	print(len(rg.visible_notes))
	#	print(self.rows_visible)
	#	print(self.score)

pyg.resource.path = ['res','res/images','res/sounds','res/fonts']
pyg.resource.reindex()

#image height = 768 width = 1024
image = pyg.resource.image('BackgroundFinal.png')
window = pyg.window.Window(width = image.width, height = image.height)

#pyg.resource.add_font('Haster.ttf')
#haster = font.load('Haster')
score = 0

pyg.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')

@window.event
def update(dt):
	game_state.update(dt)

@window.event
def on_draw():
	window.clear()
	image.blit(0,0)
	note_batch.draw()
	pressT1.draw()
	pressT2.draw()
	pressT3.draw()
	pressT4.draw()
	pressT5.draw()
	if(score != 0):
		score.draw()
	if(press[0] != 0):
		press1.draw()
	if(press[1] != 0):
		press2.draw()
	if(press[2] != 0):
		press3.draw()
	if(press[3] != 0):
		press4.draw()
	if(press[4] != 0):
		press5.draw()

@window.event
def on_key_press(symbol, modifiers):
	if(symbol == key.Z):
		keys['z'] = True
		game_state.action[0] = True
		press[0] = 1
	elif(symbol == key.X):
		keys['x'] = True
		game_state.action[1] = True
		press[1] = 1
	elif(symbol == key.C):
		keys['c'] = True
		game_state.action[2] = True
		press[2] = 1
	elif(symbol == key.V):
		keys['v'] = True
		game_state.action[3] = True
		press[3] = 1
	elif(symbol == key.B):
		keys['b'] = True
		game_state.action[4] = True
		press[4] = 1
@window.event
def on_key_release(symbol,modifiers):
	if(symbol == key.Z):
		keys['z'] = False
		press[0] = 0
	elif(symbol == key.X):
		keys['x'] = False
		press[1] = 0
	elif(symbol == key.C):
		keys['c'] = False
		press[2] = 0
	elif(symbol == key.V):
		keys['v'] = False
		press[3] = 0
	elif(symbol == key.B):
		keys['b'] = False
		press[4] = 0

if __name__ == '__main__':
	#setup buttons
	#bf.setup()

	rg = rhythm_game_env.RhythmGameEnv(song_file=sys.argv[1], diff=sys.argv[2])
	game_state = GameState()
	print(rg.title)
	print(rg.music)

	pyg.resource.path = ['res','res/images','res/sounds','res/fonts']
	pyg.resource.reindex()
	#note height = 70 width = 94
	
	note_image = pyg.resource.image('testNote.png')
	note_batch = pyg.graphics.Batch()
	notes1 = []
	notes2 = []
	notes3 = []
	notes4 = []
	notes5 = []
		
	keys = {}
	keys['z'] = False
	keys['x'] = False
	keys['c'] = False
	keys['v'] = False
	keys['b'] = False	
	yellow_image = pyg.resource.image('yellow.png')
	blue_image = pyg.resource.image('blue.png')
	green_image = pyg.resource.image('green.png')
	white_image = pyg.resource.image('white.png')
	red_image = pyg.resource.image('red.png')
	press = [0,0,0,0,0]
	press1 = pyg.sprite.Sprite(red_image, x = cheese0, y = 24)
	press2 = pyg.sprite.Sprite(yellow_image, x = cheese1, y = 24)
	press3 = pyg.sprite.Sprite(green_image, x = cheese2, y = 24)
	press4 = pyg.sprite.Sprite(blue_image, x = cheese3, y = 24)
	press5 = pyg.sprite.Sprite(white_image, x = cheese4, y = 24)
		
	yellow_image_trans = pyg.resource.image('yellowT.png')
	blue_image_trans = pyg.resource.image('blueT.png')
	green_image_trans = pyg.resource.image('greenT.png')
	white_image_trans = pyg.resource.image('whiteT.png')
	red_image_trans = pyg.resource.image('redT.png')
	pressT1 = pyg.sprite.Sprite(red_image_trans, x = cheese0, y = 24)
	pressT2 = pyg.sprite.Sprite(yellow_image_trans, x = cheese1, y = 24)
	pressT3 = pyg.sprite.Sprite(green_image_trans, x = cheese2, y = 24)
	pressT4 = pyg.sprite.Sprite(blue_image_trans, x = cheese3, y = 24)
	pressT5 = pyg.sprite.Sprite(white_image_trans, x = cheese4, y = 24)

	

	source = pyg.resource.media(rg.music)

	source.play()
	pyg.clock.schedule_interval(update, 1/180.0)
	pyg.app.run()
	#bf.cleanup()

	




