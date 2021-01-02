from browser import document, html
from browser.timer import request_animation_frame as raf
from browser.timer import cancel_animation_frame as caf
from time import time

import graphics


class Unit:
    pass


class VehicleUnit(Unit):
    def __init__(self, directional_sprite):
        self.directional_sprite = directional_sprite
        self.map_position = [0, 0]
        self.tilemap_position = [0, 0]
        self.moving = False
        self.speed = 1
        self.moving_to_tile = [0, 0]
        self.moving_total = [0, 0]

    def place_on_map(self, new_tilemap_position):
        self.tilemap_position = new_tilemap_position
        self.position = ((x * 128, y * 64) for x, y in new_tilemap_position)

    def execute_move(self, new_position):
        # print(self.map_position, self.moving_total)
        if self.moving_total[0] <= 0 or self.moving_total[1] <= 0:
            return
        self.moving_total[0] -= new_position[0] - self.map_position[0]
        self.moving_total[1] -= new_position[1] - self.map_position[1]
        self.map_position = new_position
        self.tilemap_position = new_position[0] // 128, new_position[1] // 64

    def move_to(self, moving_to_tile):
        self.moving_to_tile = moving_to_tile
        self.moving_total[0] = (moving_to_tile[0] - self.map_position[0]) * 128
        self.moving_total[1] = (moving_to_tile[1] - self.map_position[1]) * 64


class Map:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self._initialize()

    def _initialize(self):
        self.tiles = {}
        self.world = {}
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.tiles[(x, y)] = graphics.TILES["grass"]
                self.world[(x, y)] = None

    def add_unit(self, unit, tilemap_position):
        self.world[tilemap_position] = unit
        unit.place_on_map(tilemap_position)

    def world_state(self, time_now, time_delta):
        t = self.tiles
        w = self.world
        td = time_delta
        for pos, obj in w.items():
            if isinstance(obj, Unit):
                if obj.moving_to_tile != obj.tilemap_position:
                    # print(obj.tilemap_position)
                    x, y = obj.map_position
                    new_pos = x + 2, y + 1
                    obj.execute_move(new_pos)

    def draw(self, ctx, time_now, time_delta, position, screen_size):
        self.world_state(time_now, time_delta)
        cx, cy = (s // 2 for s in screen_size)
        # tiles calculations
        dx, dy = cx - 128, cy - 192
        t = self.tiles
        ctx.drawImage(t[(0, 0)].html_image, dx + 0, dy + 0)
        ctx.drawImage(t[(0, 1)].html_image, dx + 128, dy + 64)
        ctx.drawImage(t[(1, 0)].html_image, dx + 128, dy - 64)
        ctx.drawImage(t[(1, 1)].html_image, dx + 256, dy + 0)
        # sprites calculations
        # sx, sy = cx - 64, cy - 92
        # sox, soy = 0, 0 # sprite offset
        # sprite = graphics.SPRITES['bus']
        # dir = int(time_now) % 8
        # sprite.set_direction_by_index(dir)
        # if dir in [1,5]:
        #     soy += -12 #-(153-128) // 2
        # if dir in [3,7]:
        #     sox += -12 #-(153-128) // 2
        # ctx.drawImage(sprite.html_image , sx+sox, sy+soy)
        for pos, obj in self.world.items():
            if isinstance(obj, Unit):
                pos_x, pos_y = obj.map_position
                ctx.drawImage(obj.directional_sprite.html_image, pos_x, pos_y)


class Game:
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = canvas.width
        self.height = canvas.height
        self.ctx = canvas.getContext("2d", {"alpha": False})
        self.last_time = 0
        self.watchdog = False

        self.map = Map(3, 3)
        self.bus = VehicleUnit(graphics.SPRITES["bus"])
        self.map.add_unit(self.bus, (0, 0)) # map 0,0 ?
        self.bus.move_to((4, 3))
        # self.img_bus = html.IMG(src='resources/images/bus/256_0001.png')

    def clear(self):
        self.ctx.clearRect(0, 0, self.width, self.height)

    def loop(self):
        self.watchdog = True
        
        time_now = time()
        time_delta = time_now - self.last_time
        self.last_time = time_now
        
        ctx = self.ctx
        
        # clear screen
        self.clear()
        
        # map, ground
        self.map.draw(
            ctx, time_now, time_delta, (0, 0), (self.width, self.height),
        )
        
        # x = int(time_now * 50 % 150)
        # ctx.fillRect(25+x, 25+x, 50, 50)
        # ctx.drawImage(self.img_bus ,300-x, 10+x)
        
        fps = 1 // time_delta
        ctx.fillStyle = "gray";
        ctx.fillText(f"FPS: {fps}", 5, 10)
        
        self.watchdog = False


##

raf_id = None

def run(canvas):
    screen = Game(canvas)

    def abort(event=None):
        caf(raf_id)

    def keyboard(event=None):
        if event and event.keyCode == 27:
            abort(event)

    document["body"].bind("keydown", keyboard)

    def loop(i):
        global raf_id
        raf_id = raf(loop)
        if screen.watchdog:
            abort()
        screen.loop()

    loop(0)
