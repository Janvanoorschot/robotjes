import re

class Mapper(object):

    def __init__(self):
        self.width = 0
        self.height = 0
        self.map = None
        self.extras = None

    @classmethod
    def fromfile(cls, file):
        with open(file) as f:
            builder = MapBuilder()
            reader = MapReader(f, builder)
            reader.read()
            return builder.build()

class MapBuilder(object):

    def __init__(self):
        self.current_line = None
        self.maxx = 0
        self.map = []
        self.extras = []

    def extra(self,type,x,y):
        self.extras.append([type,x,y])

    def startline(self):
        self.current_line = []

    def cell(self, content):
        self.current_line.append(content)

    def endline(self):
        self.map.append(self.current_line)
        if(len(self.current_line) > self.maxx):
            self.maxx = len(self.current_line)
        self.current_line = None

    def build(self):
        mapper = Mapper()
        mapper.width = self.maxx
        mapper.height = len(self.map)
        mapper.map = self.map
        mapper.extras = self.extras
        return mapper

class MapReader(object):

    def __init__(self, f, builder):
        self.f = f
        self.builder = builder
        self.blokline = re.compile(r"""(\S+):""")
        self.extraline = re.compile(r"""(\S+)@(\d+),(\d+)""")
        self.block = None

    def read(self):
        for line in self.f:
            line = line.strip()
            if not line.startswith("#") and len(line)>0:
                blockhead = self.blokline.match(line)
                if blockhead:
                    self.block = blockhead.group(1)
                else:
                    if self.block == "extra":
                        self.extra_line(line)
                    elif self.block == "map":
                        self.map_line(line)

    def extra_line(self, line):
        extramatch = self.extraline.match(line)
        if extramatch:
            type = extramatch.group(1)
            x = int(extramatch.group(2))
            y = int(extramatch.group(3))
            self.builder.extra(type,x,y)

    def map_line(self, line):
        self.builder.startline()
        for ch in line:
            self.builder.cell(ch)
        self.builder.endline()