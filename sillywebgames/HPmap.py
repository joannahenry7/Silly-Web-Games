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
You are Harry Potter, and you, Ron and Hermione have decided
to stop Snape from getting the Philosopher's stone for Voldemort
by going through the trapdoor and getting the stone first.
Good luck!
""")


class FluffyRoom(Room):

    def machinery(self, response):
        # randomly select Fluffy's favorite notes
        notes = ["a", "b", "c", "d", "e", "f", "g"]
        fav_notes = random.sample(notes, 3)

        # check there's only 15 notes in the song
        if len(response) > 15:
            response = response[0:14]

        # check if Fluffy's favorite notes are in the song three times each
        for i in range(3):
            if response.count(fav_notes[i]) >= 3:
                next
            else:
                return 'fail'

            return 'pass'


fluffy_room = FluffyRoom("Fluffy Room",
"""
You, Ron and Hermione are in the room with Fluffy the three-headed dog.
You need to play a song to make Fluffy go to sleep. Compose a song using
the notes a, b, c, d, e, f, or g in any combination you want (you don't
have to use every note). But Fluffy will only go to sleep if he likes your
song! And each head has a favorite note that it wants to hear. The favorite
notes change every day, but each favorite note must be played multiple times
for Fluffy to like your song and fall asleep.
""")


fluffy_fail = Room("Failed",
"""
Fluffy doesn't like your song! He refuses to fall asleep!
""")


class DevilsSnareRoom(Room):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}
        self.panic = False
        self.calm = False

    def machinery(self, response):
        if response == "calm":
            self.description += """
            You remember from Herbology that Devil's Snare works more quickly
            the more you struggle so you stay calm and move as little as possible.
            """
            self.calm = True
        elif response == "panic":
            self.description += """
            You can't remember anything about Devil's Snare and you start to panic!
            The more you panic, the tighter the plant ensnares you!
            """
            self.panic = True
        elif response == "fire" and self.panic:
            self.panic = False
            self.calm = False
            return 'fail'
        elif response == "fire" and not self.calm:
            self.description += """
            You go to light a fire but the more you move, the more tightly the
            Devil's Snare wraps around you!"
            """
            self.panic = True
        elif response == "fire" and self.calm:
            self.calm = False
            return 'pass'

        return 'continue'


devils_snare_room = DevilsSnareRoom("Devil's Snare Room",
"""
Fluffy likes your song! He goes to sleep, and you, Ron and Hermione
sneak through the trap door.

You fall through the trap door onto a plant which turns out to be
Devil's Snare! The three of you become entangled in the deadly
plant! What do you do?
""")


devils_fail = Room("Failed",
"""
The Devil's Snare wraps even more tightly around you, so that
you can't even move to cast a spell!
""")


class KeyRoom(Room):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.keyspace = """
        \ro\to\to\to\to\no\to\to\to\to\no\to\to\to\to\no\to\to\to\to\no\to\to\to\to
        """
        self.keys = []
        self.key = [0, 0]
        self.paths = {}

    def machinery(self, response):

        def print_keys():
            self.keyspace = "\n\r"
            for row in self.keys:
                for i in row:
                    self.keyspace += i + "\t"
                self.keyspace += "\n"

        if len(self.keys) == 0:
            # set initial conditions
            for i in range(5):
                self.keys.append(["o"] * 5)

            h = random.randint(0,4)
            w = random.randint(0,4)
            self.key = [h, w]
            self.keys[h][w] = "F"
            print_keys()
        else:
            # reset the old key position
            h = self.key[0]
            w = self.key[1]
            self.keys[h][w] = "o"

            # move the key (make sure it doesn't go off the grid)
            h += random.randint(-1,1)
            h = max(0, min(h, 4))
            w += random.randint(-1,1)
            w = max(0, min(w, 4))
            # put key in new position and save new position
            self.keys[h][w] = "F"
            self.key = [h, w]
            print_keys()

        if response[0] == str(self.key[0]) and response[1] == str(self.key[1]):
            return 'pass'
        else:
            return 'continue'


key_room_intro = Room("Flying Key Room ",
"""
You also remember from Herbology that Devil's Snare likes the
cold and damp, so you light a fire. The plant shrinks back from
the warm flames and you, Ron and Hermione are able to escape.
You find a door and the three of you go through it.

You, Ron and Hermione enter a room filled with flying keys. There's
another door across the room, but it's locked. You need to catch the
key that opens the door using the provided broomsticks. You look at
the keys and notice one with a damaged wing. That's probably the one
you need!
""")


key_room = KeyRoom("Flying Key Room",
"""
The key can move in any direction (up, down, sideways, diagonal) but
it can only move one space at a time (or it might not move at all).
To catch the key, correctly guess where it will move next.
""")


class ChessRoom(Room):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}
        self.count = 0
        self.pawn = 1

    def machinery(self, response):
        attack = str(random.randint(0,1))
        if response == attack:
            self.description += "\nYou got a pawn!"
            self.count += 1
        else:
            self.description += "\nYou didn't get a pawn."

        self.pawn += 1

        if self.pawn > 10:
            if self.count >= 5:
                self.count = 0
                self.pawn = 1
                return 'pass'
            else:
                self.count = 0
                self.pawn = 1
                return 'fail'

        return 'continue'


chess_room = ChessRoom("Chess Room",
"""
You caught the key! Now you can open the door.

In this room is a giant chess board and you must play your way across.
Luckily Ron is basically a chess prodigy, so he can direct you and
Hermione in what to do. Ron gets most of the important chess pieces,
but he wants you to get as many pawns as possible. To attack the pawns
you must decide to either aim high or aim low. Some pawns are susceptible
to high attacks, while others are susceptible to low attacks.
You must get at least 5 pawns to win.
""")


chess_fail = Room("Failed",
"""
You didn't get enough pawns and you lose the game.
""")


class TrollRoom(Room):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}
        self.confused = False
        self.count = 0

    def machinery(self, response):
        if self.count > 3:
            self.confused = False
            self.count = 0
            return 'fail'
        elif response == 'throw':
            self.description += """
            You and Hermione start throwing anything you can find at the troll.
            It doesn't really hurt the troll, but since there are two of you
            it keeps changing its mind about who to go after.
            """
        elif response == 'yell':
            self.description += """
            You start yelling, hoping to confuse the troll. The noise echoes
            around the room and the troll can't figure out where it's coming
            from. You have successfully confused the troll!
            """
            self.confused = True
        elif response == 'wingardium leviosa' and not self.confused:
            self.description += """
            You try casting 'Wingardium Leviosa' on the troll's club (it worked
            on the troll at Halloween) but the troll has too firm a grip on its
            club! You need to distract or confuse it first.
            """
        elif response == 'wingardium leviosa' and self.confused:
            self.confused = False
            self.count = 0
            return 'pass'
        elif response == 'alohomora':
            self.description += """
            In a panic, you shout the first spell you can think of: 'ALOHOMORA!'
            To your surprise, the spell unbuttons the troll's trousers and they
            fall down, causing him to trip and fall! The troll is very disoriented.
            """
            self.confused = True
        elif response == 'lumos':
            self.description += """
            In a panic, you shout the first spell you can think of: 'LUMOS!'
            The end of your wand lights up. That's not helpful in this situation!
            """

        self.count += 1
        return 'continue'


troll_room = TrollRoom("Troll Room",
"""
You got enough pawns! You are able to win the chess game, but
Ron has to sacrifice himself in order for you to get the King.
He is knocked out by the Queen, and you and Hermione go on to
the next room without him.

You and Hermione enter a room which has a huge troll in it! The troll
is holding a large club and appears to just be waking up from being
previously knocked out. You'll have to fight it to get to the next room!
""")


troll_fail = Room("Failed",
"""
The troll becomes fed up and decides to tackle you!
""")


class PotionRoom(Room):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}
        self.bottles = [1, 2, 3, 4, 5, 6, 7]
        self.bottle = 0
        self.eliminate = []
        self.keep = []

    def machinery(self, response):
        if self.bottle == 0:
            self.bottle = random.randint(1,7)
            for i in range(7):
                bottle = self.bottles.pop()
                if str(bottle) == response or bottle == self.bottle:
                    self.keep.append(bottle)
                else:
                    self.eliminate.append(bottle)

            random.shuffle(self.eliminate)

            self.description += """
            Hermione has been able to determine from the riddle the contents
            of some of the bottles. She has been able to narrow it down to two
            of the bottles, one of which is the bottle you randomly selected.
            Hermione eliminates:
            bottle %d
            bottle %d
            bottle %d
            bottle %d
            bottle %d
            Do you want to switch to the other bottle or stick with your
            original choice?
            """ % (self.eliminate[-1], self.eliminate[-2], self.eliminate[-3],
                   self.eliminate[-4], self.eliminate[-5])

            return 'continue'
        else:
            if response == str(self.bottle):
                return 'pass'
            else:
                return 'fail'



potion_room = PotionRoom("Potion Room",
"""
While the troll is still confused, you cast 'Wingardium Leviosa'
on its club. The club soars into the air, then falls back down
on the troll's head with a huge CRACK. The troll is out cold!
You and Hermione can enter the next room.

In this room there are 7 potion bottles lined up on a table, and
fires spring up to block both the way on and the way you came.
There's a piece of parchment with a riddle about which bottle holds
the potion which will allow you to pass through the fire to go onward
or backward. Hermione starts reading the riddle, but you decide to
try picking one of the bottles at random.
Which bottle do you choose?
""")


potion_fail = Room("Failed",
"""
You picked the wrong bottle.
""")


class MirrorRoom(Room):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}
        self.distracted = False

    def machinery(self, response):
        if response == 'talk':
            self.description += """
            You try to distract Quirrell by asking him about his evil plan
            and acting sufficiently impressed. Like any good villain, he
            starts monologuing. Maybe you'll get a chance to look in the
            mirror while he's distracted!
            """
            self.distracted = True
            return 'continue'
        elif response == 'mirror' and not self.distracted:
            return 'fail'
        elif response == 'mirror' and self.distracted:
            return 'pass'


mirror_room = MirrorRoom("Mirror Room",
"""
You picked the correct bottle! But there is only enough potion
for one person, so you decide that you'll go on alone and Hermione
will go back and get Ron and try to send an owl to Dumbledore.

You enter the final room to find, to your surprise, not Professor
Snape but Professor Quirrell! He's been working for Vodemort all
along! Not only that, but Voldemort's face is stuck on the back of
Quirrell's head underneath his turban! Also in the room is the Mirror
of Erised, which you know from previous experience will show you the
thing you want most in the world.
""")


mirror_fail = Room("Failed",
"""
You try to look in the mirror but Quirrell notices what you are
up to and stops you.
""")


mirror_win = Room("The Philosopher's Stone",
"""
You know the mirror will show you what you want most in the world,
and right now what you want most in the world is to find the stone
before Quirrell, so if you look in the mirror, you should see
yourself finding it, and you'll know where it's hidden! While
Quirrell is still monologuing, you look into the mirror and see...

...yourself, holding the stone! Mirror you puts the stone in your
pocket, and miraculously, you feel the stone in your real pocket!
""")


class FinalBossBattle(Room):

    def machinery(self, response):
        win = 10

        if response == 'give up':
            return 'fail'
        elif response == 'keep fighting':
            chance = random.randint(1,10)
            if chance == win:
                return 'pass'
            else:
                self.description += """
                You keep fighting, even though your head feels like it's about
                to split open.
                """
                return 'continue'


final_boss_battle = FinalBossBattle("Battle Voldemort!",
"""
You're wondering if you can make a break for it with the stone,
when Voldemort starts talking to you from the back of Quirrell's
head. He tries to convince you to join him but you refuse because
he murdered your parents. Then he tells Quirrell to attack you,
but Quirrell can't touch you without being burned. You realize
your only hope is to hold onto Quirrell for as long as possible,
even though doing so also puts you in agonizing pain.

You grab onto Quirrell; he is being burned, but you are also in
terrible pain. You can give up, or keep fighting for as long as you
can.
""")


final_fail = Room("Failed",
"""
You just can't take any more, and stop fighting.
""")


final_win = Room("The End",
"""
You keep fighting through the pain, but eventually you pass out.

You wake up in the hospital wing with Dumbledore, who says
you held Quirrell off just long enough for him to come rescue
you! Quirrell has died, Voldemort fled, and Nicolas Flamel has
decided to destroy the Philsopher's stone to keep Voldemort from
ever getting it.

You stopped Voldemort from getting the stone! Good job!
""")


begin.add_paths({
    '*': fluffy_room
})


fluffy_room.add_paths({
    'pass': devils_snare_room,
    'fail': fluffy_fail,
    '*': fluffy_room
})


devils_snare_room.add_paths({
    'pass': key_room_intro,
    'continue': devils_snare_room,
    'fail': devils_fail,
    '*': devils_snare_room
})


key_room_intro.add_paths({
    '*': key_room
})


key_room.add_paths({
    'continue': key_room,
    'pass': chess_room,
    '*': key_room
})


chess_room.add_paths({
    'continue': chess_room,
    'pass': troll_room,
    'fail': chess_fail,
    '*': chess_room
})


troll_room.add_paths({
    'continue': troll_room,
    'pass': potion_room,
    'fail': troll_fail,
    '*': troll_room
})


potion_room.add_paths({
    'continue': potion_room,
    'pass': mirror_room,
    'fail': potion_fail,
    '*': potion_room
})


mirror_room.add_paths({
    'continue': mirror_room,
    'pass': mirror_win,
    'fail': mirror_fail,
    '*': mirror_room
})


mirror_win.add_paths({
    '*': final_boss_battle
})


final_boss_battle.add_paths({
    'continue': final_boss_battle,
    'pass': final_win,
    'fail': final_fail,
    '*': final_boss_battle
})
