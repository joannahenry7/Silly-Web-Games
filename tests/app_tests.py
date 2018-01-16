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
