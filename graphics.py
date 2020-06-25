from browser import html

import constants


class MapTile:
    URLPATH = "resources/images/terrain/"

    def __init__(self, resource):
        self.resource = resource
        self.path = self.URLPATH + constants.maptiles[resource]
        self.html_image = html.IMG(src=self.path)

    def __repr__(self):
        return "MapTile({})".format(self.resource)


TILES = {
    "water": MapTile("water"),
    "grass": MapTile("grass"),
}


class GraphicalObject:
    pass


class Vehicle(GraphicalObject):
    URLPATH = "resources/images/vehicles/"

    def __init__(self, resource):
        self.resource = resource
        self.path = {}
        self.html_image = {}
        for dir, path in constants.vehicles[resource].items():
            self.path[dir] = self.URLPATH + path
            self.html_image[dir] = html.IMG(src=self.path[dir])

    def __repr__(self):
        return "Sprite({})".format(self.resource)


class DirecionalSprite:
    def __init__(self, graphical_obj):
        self.graphical_obj = graphical_obj
        self.set_direction("SE")

    def set_direction(self, direction):
        self.html_image = self.graphical_obj.html_image[direction]
        self.direction = direction

    def set_direction_by_index(self, index):
        self.set_direction(constants.directions_map[index])


SPRITES = {
    "bus": DirecionalSprite(Vehicle("bus")),
}
