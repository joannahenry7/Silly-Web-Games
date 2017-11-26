from nose.tools import *
from sillywebgames.HPmap import *


def test_fluffy():
    path = fluffy_room.machinery("hhhhhhh")
    room = fluffy_room.go(path)
    assert_equal(room, fluffy_fail)

    # think of a way to write a better test?
    room1 = fluffy_room.go('pass')
    assert_equal(room1, devils_snare_room)

    # this should work sometimes (will fail sometimes bc can't put every note)
    # ran test; out of 10 times it failed once (too easy?? :((( maybe)
    #path1 = fluffy_room.machinery("aaabbbcccdddeee")
    #room1 = fluffy_room.go(path1)
    #assert_equal(room1, devils_snare_room)


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
