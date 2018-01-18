import random

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
You are an illustrious space pirate, flying through outer space with your crew.
You spot an interesting-looking planet that you want to explore. You fly
down and start to look around. Soon you find a cave which practically screams
'ADVENTURE!' Maybe you'll find some treasure in this cave! You and your crew
excitedly rush into the cave, fearing neither Death nor God.
""")


class SnakePit(Room):

    def machinery(self, response):
        if response == "calm":
            return 'pass'
        else:
            return 'death'


snake_pit = SnakePit("Snake Pit",
"""
You've been running through the cave-tunnel for a while when you
stumble across a snake pit. You didn't see it in time to stop so
you fall in!
""")


snake_death = Room("Death",
"""
You panic and start thrashing about wildly. You hate snakes!
The snakes react to your panic and also panic, biting you.
The snakes' venom delivers unto you a slow and agonizing death.
""")


class MonsterCave(Room):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}
        self.moved = False
        self.advantage = False
        self.disadvantage = False

    def machinery(self, response):
        if response == 'shoot' and self.moved:
            self.moved = False
            self.advantage = False
            self.disadvantage = False
            return 'death1'
        elif response == 'shoot' and self.advantage:
            self.description += """
            The monster was distracted and you managed to hit it! It moves
            away from the tunnel entrance.
            """
            self.moved = True
        elif response == 'shoot' and self.disadvantage:
            self.disadvantage = False
            return 'death1'
        elif response == 'shoot' and not self.advantage:
            self.description += """
            You shoot at the monster but it deflects the shots.
            """
            self.disadvantage = True
        elif response == 'scream':
            self.description += """
            The monster is momentarily startled! This could be your chance to shoot!
            """
            self.advantage = True
        elif response == 'poke':
            self.description += """
            The monster quivers and shrinks back from this harassment. It moves
            away from the tunnel entrance.
            """
            self.moved = True
        elif response == 'play dead':
            self.moved = False
            self.advantage = False
            self.disadvantage = False
            return 'death2'
        elif response == 'tunnel' and self.moved:
            self.moved = False
            self.advantage = False
            self.disadvantage = False
            return 'pass'
        elif response == 'tunnel' and not self.moved:
            self.description += """
            You can't go through the tunnel yet, the monster's still in the way!
            """
            self.disadvantage = True

        return 'continue'



monster_cave = MonsterCave("Monster Cave",
"""
You stay calm, and the snakes are actually pretty chill. They
really don't even move that much. They're basically large noodles.
You slowly move to the other side of the pit and climb out, then
continue down the tunnel.

You continue down the tunnel and enter a large cavernous area. At the
opposite end you see another tunnel. But standing in front of the tunnel
is a horrifying monster! It has many tentacles and eyes, and looks both
slimy and scaly. You have only one weapon with you, a small laser gun.
""")


monster_death1 = Room("Death",
"""
The monster becomes angry and disembowels you.
""")


monster_death2 = Room("Death",
"""
The monster is not fooled and crushes you with its powerful tentacles.
""")


class SpikeCave(Room):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}
        self.seelever = False
        self.tired = False
        self.count = 0

    def machinery(self, response):
        if self.count == 3:
            self.count = 0
            self.tired = False
            self.seelever = False
            return 'death1'
        elif response == 'boulder' and not self.tired:
            self.description += """
            You try to move the boulder but it's too heavy.
            """
            self.tired = True
        elif response == 'boulder' and self.tired:
            self.tired = False
            return 'death2'
        elif response == 'look':
            self.description += """
            You see no other exits but what's that, high on the cave wall? It appears
            to be a small lever! You have a length of rope, maybe you can lasso it!
            """
            self.seelever = True
        elif response == 'give up':
            self.seelever = False
            self.tired = False
            self.count = 0
            return 'death1'
        elif response == 'lasso':
            self.count += 1
            lasso_lever = random.randint(1,4)
            if lasso_lever == 1:
                self.seelever = False
                self.tired = False
                self.count = 0
                return 'pass'
            else:
                self.description += """
                You missed the lever!
                """

        return 'continue'



spike_cave = SpikeCave("Spike Cave",
"""
You run past the monster and into the tunnel!

You stumble into another cave. Immediately a boulder rolls down to seal
the way you just came in. You can see another boulder blocking a tunnel
across the cave. Spikes start slowly descending from the ceiling!

Just as you're thinking things can't get worse, water starts rising from
the floor. This is a dire predicament!
""")


spike_death1 = Room("Death",
"""
You run out of time! You die a slow, agonizing death both drowning
and being impaled by spikes.
""")


spike_death2 = Room("Death",
"""
You tire yourself out trying to move a much too heavy boulder and drown.
""")


class Bridge(Room):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}
        self.bridge = []
        self.bridgespace = """
        \r|___|\n|_0_|\n|_1_|\n|_2_|\n|_3_|\n|_4_|\n|_5_|\n|_6_|\n|_7_|\n|_8_|\n|_9_|\n|   |\n
        """
        self.count = 0
        self.rotten = []

    def machinery(self, response):

        def print_bridge():
            self.bridgespace = "\n\r"
            for row in self.bridge:
                for i in row:
                    self.bridgespace += i
                self.bridgespace += "\n"

        try:
            response = int(response)
        except:
            response = 10

        if self.count == 0:
            # set initial conditions of bridge
            self.bridge.append(['|', '_', '_', '_', '|'])
            for i in range(10):
                self.bridge.append(['|', '_', str(i), '_', '|'])
            self.bridge.append(['|', ' ', ' ', ' ', '|'])

            # assign the rotten slats
            how_many = random.randint(1,3)
            for i in range(how_many):
                slat = random.randint(0,9)
                while slat in self.rotten:
                    slat = random.randint(0,9) # make sure all slats are different
                self.rotten.append(slat)

        # test the slats
        if response in self.rotten:
            self.description += "The slat gives way! You've found a rotten one! "
            self.rotten.remove(response)
            self.bridge[(response + 1)][2] = "X"
        else:
            self.description += "The slat holds! "
            self.bridge[(response + 1)][2] = "o"

        print_bridge()

        if self.count > 4:
            self.bridge = []
            self.count = 0
            if len(self.rotten) == 0:
                self.rotten = []
                return 'pass'
            else:
                self.rotten = []
                return 'death'

        self.count += 1
        return 'continue'


bridge = Bridge("The Bridge",
"""
The boulders roll away from the tunnels and you move onward.

You come to a wide ravine with a narrow rope bridge crossing it. This
bridge doesn't look very reliable. Some of the slats might be rotten.

You find 5 rocks lying on the ground. You can test a slat by throwing
a rock on it to see if it gives way. Choose carefully though, because
you only have enough rocks to test half. To test a slat, pick a number
from 0 to 9.
""")


bridge_death = Room("Death",
"""
Your crew members cross the bridge ahead of you, but when you
try to cross a slat breaks and you fall! You plummet to your
death, smashed to pieces on the rocks below.
""")


treasure_cave = Room("The End",
"""
In the final cave you find fabulous treasure. You and your crew members
take as much as you can carry.

You leave the planet to seek more adventure and spend your hard-won treasure!
""")


begin.add_paths({
    '*': snake_pit
})


snake_pit.add_paths({
    'pass': monster_cave,
    'death': snake_death,
    '*': snake_pit
})


monster_cave.add_paths({
    'death1': monster_death1,
    'death2': monster_death2,
    'pass': spike_cave,
    'continue': monster_cave,
    '*': monster_cave
})


spike_cave.add_paths({
    'death1': spike_death1,
    'death2': spike_death2,
    'pass': bridge,
    'continue': spike_cave,
    '*': spike_cave
})


bridge.add_paths({
    'pass': treasure_cave,
    'death': bridge_death,
    'continue': bridge,
    '*': bridge
})
