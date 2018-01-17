from nose.tools import *
from sillywebgames.HPmap import *
import random


def test_fluffy():
    path = fluffy_room.machinery("hhhhhhh")
    room = fluffy_room.go(path)
    assert_equal(room, fluffy_fail)

    notes = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    random.seed(0)
    guess_notes = ''.join(random.sample(notes, 3)) * 3
    random.seed(0)
    path1 = fluffy_room.machinery(guess_notes)
    room1 = fluffy_room.go(path1)
    assert_equal(room1, devils_snare_room)


def test_devil():
    path2 = devils_snare_room.machinery("calm")
    room2 = devils_snare_room.go(path2)
    assert_equal(devils_snare_room.calm, True)
    assert_equal(devils_snare_room.panic, False)
    assert_equal(room2, devils_snare_room)
    path = devils_snare_room.machinery("fire")
    room = devils_snare_room.go(path)
    assert_equal(room, key_room_intro)
    assert "Herbology" in devils_snare_room.description
    devils_snare_room.machinery("panic")
    assert_equal(devils_snare_room.panic, True)
    assert "can't remember" in devils_snare_room.description
    path1 = devils_snare_room.machinery("fire")
    room1 = devils_snare_room.go(path1)
    assert_equal(room1, devils_fail)

def test_keys():
    room0 = key_room_intro.go('*')
    assert_equal(room0, key_room)

    random.seed(0)
    h = random.randint(0,4)
    w = random.randint(0,4)
    guess_key = str(h) + str(w)
    random.seed(0)
    path = key_room.machinery(guess_key)
    room = key_room.go(path)
    assert_equal(room, chess_room)

    path1 = key_room.machinery('55')
    room1 = key_room.go(path1)
    assert_equal(room1, key_room)

def test_chess():
    pawns = [1, 1, 0, 0, 1, 0, 1, 0, 0, 1]
    random.seed(0)
    for pawn in pawns:
        path = chess_room.machinery(str(pawn))
    assert 'You got a pawn!' in chess_room.description
    room = chess_room.go(path)
    assert_equal(room, troll_room)

    for i in range(10):
        path1 = chess_room.machinery('2')
    assert "You didn't get a pawn." in chess_room.description
    room1 = chess_room.go(path1)
    assert_equal(room1, chess_fail)

def test_troll():
    path = troll_room.machinery('throw')
    room = troll_room.go(path)
    assert_equal(room, troll_room)
    assert_equal(troll_room.count, 1)
    assert 'You and Hermione start throwing' in troll_room.description
    path1 = troll_room.machinery('alohomora')
    room1 = troll_room.go(path1)
    assert_equal(troll_room.confused, True)
    assert_equal(troll_room.count, 2)
    path2 = troll_room.machinery('lumos')
    room2 = troll_room.go(path2)
    assert_equal(troll_room.count, 3)
    assert 'The end of your wand lights up' in troll_room.description
    path3 = troll_room.machinery('yell')
    room3 = troll_room.go(path3)
    assert 'You start yelling,' in troll_room.description
    assert_equal(troll_room.count, 4)
    path4 = troll_room.machinery('wingardium leviosa')
    room4 = troll_room.go(path4)
    assert_equal(room4, troll_fail)
    assert_equal(troll_room.count, 0)
    assert_equal(troll_room.confused, False)

    path5 = troll_room.machinery('alohomora')
    room5 = troll_room.go(path5)
    path6 = troll_room.machinery('wingardium leviosa')
    room6 = troll_room.go(path6)
    assert_equal(room6, potion_room)

def test_potion():
    random.seed(0)
    guess_bottle = str(random.randint(1,7))
    random.seed(0)
    path = potion_room.machinery(guess_bottle)
    room = potion_room.go(path)
    assert_equal(room, potion_room)
    assert 'Hermione has been able to determine' in potion_room.description
    path1 = potion_room.machinery(guess_bottle)
    room1 = potion_room.go(path1)
    assert_equal(room1, mirror_room)

    potion_room.machinery('0')
    path3 = potion_room.machinery('0')
    room3 = potion_room.go(path3)
    assert_equal(room3, potion_fail)

def test_mirror():
    pass
