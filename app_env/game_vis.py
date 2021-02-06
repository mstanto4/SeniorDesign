import pyglet
pyglet.resource.path = ['res','res/images','res/sounds','res/fonts']
pyglet.resource.reindex()

#image height = 656 width = 1500
image = pyglet.resource.image('testBackground.jpg')
window = pyglet.window.Window(width = image.width, height = image.height)



@window.event
def on_draw():
	window.clear()
	image.blit(0,0)

pyglet.app.run()






