from nose.tools import *
from sillywebgames.piratemap import *
import random


def test_snake_pit():
    # test getting from beginning to snake pit
    room0 = begin.go('*')
    assert_equal(room0, snake_pit)

    # test successully passing snake pit
    path = snake_pit.machinery('calm')
    room = snake_pit.go(path)
    assert_equal(room, monster_cave)

    # test dying in snake pit
    path1 = snake_pit.machinery('panic')
    room1 = snake_pit.go(path1)
    assert_equal(room1, snake_death)

def test_monster_cave():
    # may need to rewrite these tests if change piratemap like HPmap was changed
    # check shooting first turns on 'disadvantage' parameter
    assert_equal(monster_cave.disadvantage, False)
    path = monster_cave.machinery('shoot')
    room = monster_cave.go(path)
    assert_equal(room, monster_cave)
    assert_equal(monster_cave.disadvantage, True)

    # check screaming turns on 'advantage' parameter
    assert_equal(monster_cave.advantage, False)
    path1 = monster_cave.machinery('scream')
    room1 = monster_cave.go(path1)
    assert_equal(room1, monster_cave)
    assert_equal(monster_cave.advantage, True)

    # check poking monster makes it move
    assert_equal(monster_cave.moved, False)
    path2 = monster_cave.machinery('poke')
    room2 = monster_cave.go(path2)
    assert_equal(room2, monster_cave)
    assert_equal(monster_cave.moved, True)

    # test failing by playing dead
    path3 = monster_cave.machinery('play dead')
    room3 = monster_cave.go(path3)
    assert_equal(room3, monster_death2)

    # test successfully getting past monster (monster is still moved from previous turn)
    path4 = monster_cave.machinery('tunnel')
    room4 = monster_cave.go(path4)
    assert_equal(room4, spike_cave)

    # test failing by shooting monster after it moves
    path5 = monster_cave.machinery('shoot')
    room5 = monster_cave.go(path5)
    assert_equal(room5, monster_death1)

def test_spike_cave():
    # test failing by trying to move the boulder twice
    assert_equal(spike_cave.tired, False)
    path = spike_cave.machinery('boulder')
    room = spike_cave.go(path)
    assert_equal(room, spike_cave)
    assert_equal(spike_cave.tired, True)
    path1 = spike_cave.machinery('boulder')
    room1 = spike_cave.go(path1)
    assert_equal(room1, spike_death2)

    # test successfully lassoing lever
    assert_equal(spike_cave.seelever, False)
    path2 = spike_cave.machinery('look')
    room2 = spike_cave.go(path2)
    assert_equal(spike_cave.seelever, True)
    random.seed(1) # this seed makes lasso attempt successful
    path3 = spike_cave.machinery('lasso')
    room3 = spike_cave.go(path3)
    assert_equal(room3, bridge)

    # test failing by not lassoing lever
    random.seed(0) # this seed makes first 4 lasso attempts unsuccessful
    path4 = spike_cave.machinery('lasso')
    room4 = spike_cave.go(path4)
    assert_equal(room4, spike_cave)
    assert_equal(spike_cave.count, 1)
    assert 'You missed the lever!' in spike_cave.description
    for i in range(3):
        path5 = spike_cave.machinery('lasso')
        room5 = spike_cave.go(path5)
    assert_equal(room5, spike_death1)

    # test failing by giving up
    path6 = spike_cave.machinery('give up')
    room6 = spike_cave.go(path6)
    assert_equal(room6, spike_death1)

def test_bridge():
    pass
