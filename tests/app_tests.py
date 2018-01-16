from nose.tools import *
from bin.app import app
from tests.tools import assert_response
import random


# allows you to return to specific session to test progress through game
def get_session_id(resp):
    cookies_str = resp.headers['Set-Cookie']
    if cookies_str:
        for kv in cookies_str.split(';'):
            if 'webpy_session_id=' in kv:
                return kv

def test_index():
    # check that we get a 404 on non-existent url
    resp = app.request('/h')
    assert_response(resp, status='404')

    # check / url
    resp1 = app.request('/')
    assert_response(resp1, contains='Which game')

    # check that selecting a game redirects to that game
    data = {'game': 'Harry Potter Game'}
    resp2 = app.request('/', method='POST', data=data)
    assert_response(resp2, status='303')
    session_id = get_session_id(resp2)
    header = {'Cookie': session_id}
    resp3 = app.request('/HPGame', headers=header)
    assert_response(resp3, contains='You are Harry Potter')

    data1 = {'game': 'Pirate Game'}
    resp4 = app.request('/', method='POST', data=data1)
    assert_response(resp4, status='303')
    session_id1 = get_session_id(resp4)
    header1 = {'Cookie': session_id1}
    resp5 = app.request('/PirateGame', headers=header1)
    assert_response(resp5, contains='You are an illustrious space pirate')

def test_success_hp():
    # initialize and navigate to Fluffy Room
    data0 = {'game': 'Harry Potter Game'}
    resp = app.request('/', method='POST', data=data0)
    session_id = get_session_id(resp)
    header = {'Cookie': session_id}
    app.request('/HPGame', headers=header, method='POST')

    # check we have arrived at the Fluffy Room
    resp1 = app.request('/HPGame', headers=header)
    assert_response(resp1, contains='Fluffy Room')

    # check song passes; use random.seed to make sure random sample is predictable
    notes = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    random.seed(0)
    guess_notes = ''.join(random.sample(notes, 3)) * 3
    data = {'action': guess_notes}
    random.seed(0)
    resp2 = app.request('/HPGame', headers=header, method='POST', data=data)
    assert_response(resp2, status='303')
    resp3 = app.request('/HPGame', headers=header)
    assert_response(resp3, contains="Fluffy likes your song!")

    # check getting past devils snare
    data1 = {'action': 'calm'}
    data2 = {'action': 'fire'}
    resp4 = app.request('/HPGame', headers=header, method='POST', data=data1)
    assert_response(resp4, status='303')
    resp5 = app.request('/HPGame', headers=header)
    assert_response(resp5, contains='You remember from Herbology')
    resp6 = app.request('/HPGame', headers=header, method='POST', data=data2)
    assert_response(resp6, status='303')
    resp7 = app.request('/HPGame', headers=header)
    assert_response(resp7, contains='Flying Key Room')

    # check getting past key room
    resp8 = app.request('/HPGame', headers=header, method='POST')
    assert_response(resp8, status='303')
    resp9 = app.request('/HPGame', headers=header)
    assert_response(resp9, contains="The key can move in any direction")
    random.seed(0)
    h = random.randint(0,4)
    w = random.randint(0,4)
    guess_key = str(h) + str(w)
    data3 = {'action': guess_key}
    random.seed(0)
    resp10 = app.request('/HPGame', headers=header, method='POST', data=data3)
    assert_response(resp10, status='303')
    resp11 = app.request('/HPGame', headers=header)
    assert_response(resp11, contains='Chess Room')

    # check getting past chess room
    pawns = []
    random.seed(0)
    for i in range(10):
        pawns.append(random.randint(0,1))
    random.seed(0)
    for pawn in pawns:
        data = {'action': str(pawn)}
        app.request('/HPGame', headers=header, method='POST', data=data)
    resp12 = app.request('/HPGame', headers=header)
    assert_response(resp12, contains='Troll Room')

    # check getting past troll room
    data4 = {'action': 'yell'}
    app.request('/HPGame', headers=header, method='POST', data=data4)
    resp13 = app.request('/HPGame', headers=header)
    assert_response(resp13, contains='You start yelling')
    data5 = {'action': 'wingardium leviosa'}
    app.request('/HPGame', headers=header, method='POST', data=data5)
    resp14 = app.request('/HPGame', headers=header)
    assert_response(resp14, contains='Potion Room')

    # check getting past potion room
    random.seed(0)
    data6 = {'action': str(random.randint(1,7))}
    random.seed(0)
    app.request('/HPGame', headers=header, method='POST', data=data6)
    resp15 = app.request('/HPGame', headers=header)
    assert_response(resp15, contains='Hermione has been able to determine')
    app.request('/HPGame', headers=header, method='POST', data=data6)
    resp16 = app.request('/HPGame', headers=header)
    assert_response(resp16, contains='Mirror Room')

    # check getting past mirror room
    data7 = {'action': 'talk'}
    app.request('/HPGame', headers=header, method='POST', data=data7)
    resp17 = app.request('/HPGame', headers=header)
    assert_response(resp17, contains='You try to distract Quirrell')
    data8 = {'action': 'mirror'}
    app.request('/HPGame', headers=header, method='POST', data=data8)
    resp18 = app.request('/HPGame', headers=header)
    assert_response(resp18, contains='You know the mirror will show you')

    # get to Battle Voldemort room and battle Voldemort
    app.request('/HPGame', headers=header, method='POST')
    resp19 = app.request('/HPGame', headers=header)
    assert_response(resp19, contains='Battle Voldemort!')
    data9 = {'action': 'keep fighting'}
    random.seed(2) # this seed makes first random.randint match winning number
    app.request('/HPGame', headers=header, method='POST', data=data9)
    resp20 = app.request('/HPGame', headers=header)
    assert_response(resp20, contains='You keep fighting through the pain')

def test_fail_hp():
    # initialize and navigate to Fluffy Room
    def go_to_fluffy():
        data0 = {'game': 'Harry Potter Game'}
        resp = app.request('/', method='POST', data=data0)
        session_id = get_session_id(resp)
        header = {'Cookie': session_id}
        app.request('/HPGame', headers=header, method='POST')
        return header

    # check failing in fluffy room
    header = go_to_fluffy()
    data = {'action': 'hhhhhhhhhh'}
    app.request('/HPGame', headers=header, method='POST', data=data)
    resp1 = app.request('/HPGame', headers=header)
    assert_response(resp1, contains='He refuses to fall asleep!')

    def get_past_fluffy(header):
        notes = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        random.seed(0)
        guess_notes = ''.join(random.sample(notes, 3)) * 3
        data = {'action': guess_notes}
        random.seed(0)
        app.request('/HPGame', headers=header, method='POST', data=data)

    # check failing in devils snare room (both ways to fail)
    header1 = go_to_fluffy()
    get_past_fluffy(header1)
    data1 = {'action': 'panic'}
    data2 = {'action': 'fire'}
    app.request('/HPGame', headers=header1, method='POST', data=data1)
    resp2 = app.request('/HPGame', headers=header1)
    assert_response(resp2, contains='you start to panic!')
    app.request('/HPGame', headers=header1, method='POST', data=data2)
    resp3 = app.request('/HPGame', headers=header1)
    assert_response(resp3, contains='wraps even more tightly around you')
    header2 = go_to_fluffy()
    get_past_fluffy(header2)
    app.request('/HPGame', headers=header2, method='POST', data=data2)
    resp4 = app.request('/HPGame', headers=header2)
    assert_response(resp4, contains='You go to light a fire but')

    def get_past_devil(header):
        data1 = {'action': 'calm'}
        data2 = {'action': 'fire'}
        app.request('/HPGame', headers=header, method='POST', data=data1)
        app.request('/HPGame', headers=header, method='POST', data=data2)
        app.request('/HPGame', headers=header, method='POST') # gets past key room intro

    # check failing in key room (not moving on is failing for this room)
    header3 = go_to_fluffy()
    get_past_fluffy(header3)
    get_past_devil(header3)
    data3 = {'action': '55'}
    app.request('/HPGame', headers=header3, method='POST', data=data3)
    resp5 = app.request('/HPGame', headers=header3)
    assert_response(resp5, contains='The key can move in any direction')

    def get_past_keys(header):
        random.seed(0)
        h = random.randint(0,4)
        w = random.randint(0,4)
        guess_key = str(h) + str(w)
        data = {'action': guess_key}
        random.seed(0)
        app.request('/HPGame', headers=header, method='POST', data=data)

    # check failing in chess room
    header4 = go_to_fluffy()
    get_past_fluffy(header4)
    get_past_devil(header4)
    get_past_keys(header4)
    data4 = {'action': '2'}
    for i in range(10):
        app.request('/HPGame', headers=header4, method='POST', data=data4)
    resp6 = app.request('/HPGame', headers=header4)
    assert_response(resp6, contains='t get enough pawns and you lose')

    def get_past_chess(header):
        pawns = []
        random.seed(0)
        for i in range(10):
            pawns.append(random.randint(0,1))
        random.seed(0)
        for pawn in pawns:
            data = {'action': str(pawn)}
            app.request('/HPGame', headers=header, method='POST', data=data)

    # check failing in troll room
    header5 = go_to_fluffy()
    get_past_fluffy(header5)
    get_past_devil(header5)
    get_past_keys(header5)
    get_past_chess(header5)
    data5 = {'action': 'throw'}
    data6 = {'action': 'lumos'}
    data7 = {'action': 'wingardium leviosa'}
    data8 = {'action': 'alohomora'}
    app.request('/HPGame', headers=header5, method='POST', data=data5)
    resp7 = app.request('/HPGame', headers=header5)
    assert_response(resp7, contains='You and Hermione start throwing anything')
    app.request('/HPGame', headers=header5, method='POST', data=data6)
    resp8 = app.request('/HPGame', headers=header5)
    assert_response(resp8, contains='The end of your wand lights up.')
    app.request('/HPGame', headers=header5, method='POST', data=data7)
    resp9 = app.request('/HPGame', headers=header5)
    assert_response(resp9, contains='the troll has too firm a grip')
    app.request('/HPGame', headers=header5, method='POST', data=data8)
    resp10 = app.request('/HPGame', headers=header5)
    assert_response(resp10, contains='To your surprise, the spell unbuttons')
    app.request('/HPGame', headers=header5, method='POST', data=data5)
    resp11 = app.request('/HPGame', headers=header5)
    assert_response(resp11, contains='The troll becomes fed up')

    def get_past_troll(header):
        data1 = {'action': 'yell'}
        app.request('/HPGame', headers=header, method='POST', data=data1)
        data2 = {'action': 'wingardium leviosa'}
        app.request('/HPGame', headers=header, method='POST', data=data2)

    # check failing in potion room
    header6 = go_to_fluffy()
    get_past_fluffy(header6)
    get_past_devil(header6)
    get_past_keys(header6)
    get_past_chess(header6)
    get_past_troll(header6)
    data9 = {'action': '0'}
    app.request('/HPGame', headers=header6, method='POST', data=data9)
    resp12 = app.request('/HPGame', headers=header6)
    assert_response(resp12, contains='Hermione has been able to determine')
    app.request('/HPGame', headers=header6, method='POST', data=data9)
    resp13 = app.request('/HPGame', headers=header6)
    assert_response(resp13, contains='You picked the wrong bottle.')

    def get_past_potion(header):
        random.seed(0)
        data = {'action': str(random.randint(1,7))}
        random.seed(0)
        app.request('/HPGame', headers=header, method='POST', data=data)
        app.request('/HPGame', headers=header, method='POST', data=data)

    # check failing in mirror room
    header7 = go_to_fluffy()
    get_past_fluffy(header7)
    get_past_devil(header7)
    get_past_keys(header7)
    get_past_chess(header7)
    get_past_troll(header7)
    get_past_potion(header7)
    data10 = {'action': 'mirror'}
    app.request('/HPGame', headers=header7, method='POST', data=data10)
    resp14 = app.request('/HPGame', headers=header7)
    assert_response(resp14, contains='You try to look in the mirror but')

    def get_past_mirror(header):
        data1 = {'action': 'talk'}
        app.request('/HPGame', headers=header, method='POST', data=data1)
        data2 = {'action': 'mirror'}
        app.request('/HPGame', headers=header, method='POST', data=data2)
        app.request('/HPGame', headers=header, method='POST') # gets past plot exposition

    # check failure in battle voldemort
    header8 = go_to_fluffy()
    get_past_fluffy(header8)
    get_past_devil(header8)
    get_past_keys(header8)
    get_past_chess(header8)
    get_past_troll(header8)
    get_past_potion(header8)
    get_past_mirror(header8)
    data11 = {'action': 'keep fighting'}
    data12 = {'action': 'give up'}
    random.seed(0)
    app.request('/HPGame', headers=header8, method='POST', data=data11)
    resp15 = app.request('/HPGame', headers=header8)
    assert_response(resp15, contains='You keep fighting, even though')
    app.request('/HPGame', headers=header8, method='POST', data=data12)
    resp16 = app.request('/HPGame', headers=header8)
    assert_response(resp16, contains='stop fighting.')
