from flask import json
from random import randrange

def test_home(client):
    r=client.get('/')
    assert r.status_code == 200

def test_users_post(client):
    n = randrange(0,99999)
    n_string = str(n)
    username = 'zaza'+n_string
    email = 'zaza@zaza.com'+n_string
    j = {'username': username, 'email': email}
    r = client.post('/users', data=json.dumps(j), content_type='application/json')
    assert r.status_code == 200
    assert  r.json['id'] is not None
    assert  type(r.json['id']) is int
    global user_id
    user_id = str(r.json['id'])
    assert  r.json['username'] is not None
    assert  type(r.json['username']) is str
    assert  r.json['username'] == username

    assert  r.json['email'] is not None
    assert  type(r.json['email']) is str
    assert  r.json['email'] == email

    r = client.post('/users', data=json.dumps(j), content_type='application/json')#dumps trasforma un json in dictionary
    assert  r.status_code == 400


def test_users_get(client):
    r=client.get('/users')
    assert r.status_code == 200

def test_users_delete(client):
    '''test delete a user'''
    r = client.delete("/users/"+user_id)
    assert  r.status_code == 200
    r = client.delete("/users/9999")
    assert r.status_code == 404