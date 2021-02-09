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

		print(rg.visible_notes)

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
	notes1.append(pyg.sprite.Sprite(note_image, x = 290, y = 350, batch=note_batch))
	notes2.append(pyg.sprite.Sprite(note_image, x = 510, y = 350, batch=note_batch))
	notes3.append(pyg.sprite.Sprite(note_image, x = 700, y = 350, batch=note_batch))
	notes4.append(pyg.sprite.Sprite(note_image, x = 875, y = 350, batch=note_batch))
	notes5.append(pyg.sprite.Sprite(note_image, x = 1075, y = 350, batch=note_batch))
	
	pyg.clock.schedule_interval(update, 1/120.0)
	pyg.app.run()






