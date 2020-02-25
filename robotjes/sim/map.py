import re

class Map(object):
    """ An immutabel representation of the map of a maze."""

    def __init__(self):
        self.height = 0
        self.width = 0
        self.extras = []
        self.extras_type = {}
        self.paints_black = []
        self.paints_black_type = {}
        self.paints_white = []
        self.paints_white_type = {}
        self.tiles = []
        self.tiles_type = {}
        self.startposses = []
        self.beacons = []

    def start_positions(self):
        return list(self.startposses)

    def paints_blacks(self):
        return list(self.paints_black)

    def paints_whites(self):
        return list(self.paints_white)

    def start_beacons(self):
        return list(self.beacons)

    def contains_pos(self, pos):
        return pos[0]>=0 and pos[0]<self.width and pos[1]>=0 and pos[1]<self.height

    @classmethod
    def fromfile(cls, file):
        with open(file) as f:
            builder = MapBuilder()
            reader = MapReader(f, builder)
            reader.read()
            return builder.build()

class MapBuilder(object):

    def __init__(self):
        self.height = 0
        self.width = 0
        self.extras = []
        self.extras_type = {}
        self.paints_black = []
        self.paints_black_type = {}
        self.paints_white = []
        self.paints_white_type = {}
        self.tiles = []
        self.tiles_type = {}
        self.startposses = []
        self.beacons = []

    def extra(self,type,x,y):
        self.extras.append((x,y))
        self.extras_type[(x,y)] = type

    def paint(self,color,type,x,y):
        if color == "b":
            self.paints_black.append((x,y))
            self.paints_black_type[(x,y)] = type
        else:
            self.paints_white.append((x,y))
            self.paints_white_type[(x,y)] = type

    def beacon(self, x, y):
        self.coord(x,y)
        self.beacons.append((x,y))

    def startpos(self, x, y):
        self.coord(x,y)
        self.startposses.append((x,y))

    def tile(self, x, y, t):
        self.coord(x,y)
        self.tiles.append((x,y))
        self.tiles_type[(x,y)] = t

    def coord(self, x, y):
        if self.width < x:
            self.width = x
        if self.height < y:
            self.height = y

    def build(self):
        mapper = Map()
        mapper.width = self.width
        mapper.height = self.height
        mapper.extras = self.extras
        mapper.extras_type = self.extras_type
        mapper.paints_black = self.paints_black
        mapper.paints_black_type = self.paints_black_type
        mapper.paints_white = self.paints_white
        mapper.paints_white_type = self.paints_white_type
        mapper.tiles = self.tiles
        mapper.tiles_type = self.tiles_type
        mapper.startposses = self.startposses
        mapper.beacons = self.beacons
        return mapper

class MapReader(object):

    def __init__(self, f, builder):
        self.f = f
        self.builder = builder
        self.blokline = re.compile(r"""(\S+):""")
        self.extraline = re.compile(r"""(\S+)@(\d+),(\d+)""")
        self.paintline = re.compile(r"""\s*([wb])\s*,\s*([.\-|])\s*,\s*(\d+)\s*,\s*(\d+)\s*""")
        self.section = None
        self.nextx = 0
        self.nexty = 0

    def read(self):
        for line in self.f:
            line = line.strip()
            if not line.startswith("#") and len(line)>0:
                blockhead = self.blokline.match(line)
                if blockhead:
                    section = blockhead.group(1)
                    if section == 'extra':
                        self.section = 'extra'
                    elif section == 'map':
                        self.section = 'map'
                    elif section == 'paint':
                        self.section = 'paint'
                else:
                    if self.section == "extra":
                        self.extra_line(line)
                    elif self.section == "map":
                        self.map_line(line)
                    elif self.section == 'paint':
                        self.paint_line(line)

    def extra_line(self, line):
        extramatch = self.extraline.match(line)
        if extramatch:
            type = extramatch.group(1)
            x = int(extramatch.group(2))
            y = int(extramatch.group(3))
            self.builder.extra(type,x,y)

    def map_line(self, line):
        self.nextx = 0
        for ch in line:
            if ch == '@':
                self.builder.startpos(self.nextx, self.nexty)
                self.nextx = self.nextx + 1
            elif ch == '*':
                    self.builder.beacon(self.nextx, self.nexty)
                    self.nextx = self.nextx + 1
            elif ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    self.builder.tile(self.nextx, self.nexty, ch)
                    self.nextx = self.nextx + 1
        self.nexty = self.nexty + 1

    def paint_line(self, line):
        all = re.findall("\((.*?)\)", line)
        for item in all:
            paintmatch = self.paintline.match(item)
            if paintmatch:
                color = paintmatch.group(1)
                type = paintmatch.group(2)
                x = int(paintmatch.group(3))
                y = int(paintmatch.group(4))
                self.builder.paint(color,type,x,y)

