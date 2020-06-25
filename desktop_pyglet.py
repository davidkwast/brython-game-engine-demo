import math
import pyglet

window = pyglet.window.Window(resizable=True)
window.maximize()
window.set_location(0, 0)
window.set_size(1280, 720)

image_bus = pyglet.resource.image('resources/images/vehicles/bus/256_0001.png')
image_grass = pyglet.resource.image('resources/images/terrain/grass/256_0001.png')

batch = pyglet.graphics.Batch()

sprite_grass = pyglet.sprite.Sprite(img=image_grass, batch=batch)
sprite_grass.x, sprite_grass.y = 0, 720-128

sprite_bus_01 = pyglet.sprite.Sprite(img=image_bus, batch=batch)
sprite_bus_01.y = 720-128
sprite_bus_01.fx, sprite_bus_01.fy = float(sprite_bus_01.x), float(sprite_bus_01.y)

# fps_display = pyglet.window.FPSDisplay(window)
@window.event
def on_draw():
    window.clear()
    batch.draw()
    # fps_display.draw()

def update(dt):
    s = sprite_bus_01
    s.fx = (s.fx + dt*60) % 600
    s.fy = s.fy - dt*30
    if s.fy < -128:
         s.fy = 720-128
    s.x, s.y = int(s.fx), int(s.fy)

# pyglet.clock.set_fps_limit(60)
pyglet.clock.schedule_interval(update, 0.015)
pyglet.app.run()
