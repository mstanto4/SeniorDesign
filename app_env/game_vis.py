import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')
import rhythm_game_env
import numpy as np
import pyglet as pyg

pyg.resource.path = ['res','res/images','res/sounds','res/fonts']
pyg.resource.reindex()

#image height = 656 width = 1500
image = pyg.resource.image('testBackground.jpg')
window = pyg.window.Window(width = image.width, height = image.height)

#note height = 70 width = 94
note_image = pyg.resource.image('testNote.png')
notes = []
notes.append(pyg.sprite.Sprite(note_image, x = 290, y = 350))
notes.append(pyg.sprite.Sprite(note_image, x = 510, y = 350))
notes.append(pyg.sprite.Sprite(note_image, x = 700, y = 350))
notes.append(pyg.sprite.Sprite(note_image, x = 875, y = 350))
notes.append(pyg.sprite.Sprite(note_image, x = 1075, y = 350))


@window.event
def on_draw():
	window.clear()
	image.blit(0,0)
	for note in notes:
		note.draw()

pyg.app.run()






