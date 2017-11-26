class Room(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}

    def go(self, direction):
        return self.paths.get(direction)

    def add_paths(self, paths):
        self.paths.update(paths)


begin = Room("Begin",
"""
You are an illustrious space pirate flying through outer
space with your crew.
""")
