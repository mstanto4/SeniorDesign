import pyglet
pyglet.resource.path = ['res','res/images','res/sounds','res/fonts']
pyglet.resource.reindex()

#image height = 656 width = 1500
image = pyglet.resource.image('testBackground.jpg')
window = pyglet.window.Window(width = image.width, height = image.height)

#note height = 70 width = 94
note_image = pyglet.resource.image('testNote.png')
notes = []
notes.append(pyglet.sprite.Sprite(note_image, x = 290, y = 350))
notes.append(pyglet.sprite.Sprite(note_image, x = 510, y = 350))
notes.append(pyglet.sprite.Sprite(note_image, x = 700, y = 350))
notes.append(pyglet.sprite.Sprite(note_image, x = 875, y = 350))
notes.append(pyglet.sprite.Sprite(note_image, x = 1075, y = 350))


@window.event
def on_draw():
	window.clear()
	image.blit(0,0)
	for note in notes:
		note.draw()

pyglet.app.run()






