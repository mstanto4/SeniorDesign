#for including gym / probably wont need or will need to change on pi
import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')

import rhythm_game_env
import numpy as np
import pyglet as pyg

class GameState():
	def __init__(self):	
		self.done = False
		self.score = 0
		self.reward = 0
		self.state = []
		self.blank_note = [False for x in range(5)]
		self.action = self.blank_note
		self.rows_visible = 0

	def update(self, dt):
		prev_state = self.state
		self.done, self.reward, self.state = rg.step(self.action)
		self.score += self.reward

		if self.reward < 0:
			print("Action:", self.action)
			print("State:", prev_state)
			print("Reward:", self.reward)

			if self.action != list(prev_state[0]):
				print("Mismatch detected.")

			print()

		if self.state[1] <= rg.perfect_threshold:
			self.action = list(self.state[0])

		else:
			self.action = self.blank_note
		
		if(len(rg.visible_notes) > self.rows_visible):
			self.rows_visible += 1
			if(rg.visible_notes[len(rg.visible_notes)-1][0] == True):
				notes1.append(pyg.sprite.Sprite(note_image, x = 290, y = 350, batch=note_batch))
			if(rg.visible_notes[len(rg.visible_notes)-1][1] == True):
				notes2.append(pyg.sprite.Sprite(note_image, x = 510, y = 350, batch=note_batch))
			if(rg.visible_notes[len(rg.visible_notes)-1][2] == True):
				notes3.append(pyg.sprite.Sprite(note_image, x = 700, y = 350, batch=note_batch))
			if(rg.visible_notes[len(rg.visible_notes)-1][3] == True):
				notes4.append(pyg.sprite.Sprite(note_image, x = 875, y = 350, batch=note_batch))
			if(rg.visible_notes[len(rg.visible_notes)-1][4] == True):
				notes5.append(pyg.sprite.Sprite(note_image, x = 1075, y = 350, batch=note_batch))
		elif(len(rg.visible_notes) < self.rows_visible):
			self.rows_visible -= 1	
		
		#delete notes
		count = [0,0,0,0,0]
		for num, row in enumerate(rg.visible_notes):
			for which, note in enumerate(row):
				if(note == True):
					count[which] += 1

		if(count[0] < len(notes1)):
			notes1[0].delete()
			del notes1[0]			
		if(count[1] < len(notes2)):
			notes2[0].delete()
			del notes2[0]			
		if(count[2] < len(notes3)):
			notes3[0].delete()
			del notes3[0]			
		if(count[3] < len(notes4)):
			notes4[0].delete()
			del notes4[0]			
		if(count[4] < len(notes5)):
			notes5[0].delete()
			del notes5[0]			
	
		for num, row in enumerate(rg.visible_notes):
			for which, note in enumerate(row):
				one = 0
				two = 0
				three = 0
				four = 0
				five = 0
				if(note == True):
					if(which == 0):
						notes1[one].y = 350 - (192 - rg.visible_note_distances[num]) 
						one += 1			
					if(which == 1):
						notes2[two].y = 350 - (192 - rg.visible_note_distances[num]) 
						two += 1			
					if(which == 2):
						notes3[three].y = 350 - (192 - rg.visible_note_distances[num]) 
						three += 1			
					if(which == 3):
						notes4[four].y = 350 - (192 - rg.visible_note_distances[num]) 
						four += 1			
					if(which == 4):
						notes5[five].y = 350 - (192 - rg.visible_note_distances[num]) 
						five += 1			
	
		print(rg.visible_notes)
		print(len(rg.visible_notes))
		print(self.rows_visible)

pyg.resource.path = ['res','res/images','res/sounds','res/fonts']
pyg.resource.reindex()

#image height = 656 width = 1500
image = pyg.resource.image('testBackground.jpg')
window = pyg.window.Window(width = image.width, height = image.height)

def update(dt):
	game_state.update(dt)

@window.event
def on_draw():
	window.clear()
	image.blit(0,0)
	note_batch.draw()

if __name__ == '__main__':
	rg = rhythm_game_env.RhythmGameEnv(song_file=sys.argv[1], diff=sys.argv[2])
	game_state = GameState()

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
	
	pyg.clock.schedule_interval(update, 1/240.0)
	pyg.app.run()






