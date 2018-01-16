from nose.tools import *
from sillywebgames.piratemap import *


def test_snake_pit():
    room0 = begin.go('*')
    assert_equal(room0, snake_pit)
    path = snake_pit.machinery('calm')
    room = snake_pit.go(path)
    assert_equal(room, monster_cave)
    path1 = snake_pit.machinery('panic')
    room1 = snake_pit.go(path1)
    assert_equal(room1, snake_death)

def test_monster_cave():
    assert_equal(monster_cave.disadvantage, False)
    path = monster_cave.machinery('shoot')
    room = monster_cave.go(path)
    assert_equal(room, monster_cave)
    assert_equal(monster_cave.disadvantage, True)
    assert_equal(monster_cave.advantage, False)
    path1 = monster_cave.machinery('scream')
    room1 = monster_cave.go(path1)
    assert_equal(room1, monster_cave)
    assert_equal(monster_cave.advantage, True)
    assert_equal(monster_cave.moved, False)
    path2 = monster_cave.machinery('poke')
    room2 = monster_cave.go(path2)
    assert_equal(room2, monster_cave)
    assert_equal(monster_cave.moved, True)
    path3 = monster_cave.machinery('play dead')
    room3 = monster_cave.go(path3)
    assert_equal(room3, monster_death2)
    path4 = monster_cave.machinery('tunnel')
    room4 = monster_cave.go(path4)
    assert_equal(room4, spike_cave)
    path5 = monster_cave.machinery('shoot')
    room5 = monster_cave.go(path5)
    assert_equal(room5, monster_death1)

def test_spike_room():
    pass
