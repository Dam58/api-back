from flask import json, jsonify
from random import randrange
from app import User, ModelSchema, user_schema, users_schema

n = randrange(0,100)

def test_home(client):
    r=client.get('/')
    r.status == '200'

def test_get(client):
    r=client.get('https://api8bigfiish88.herokuapp.com/api/v1.0/users?page=1')
    r.status == '200'

def test_get1(client):
    user = User.query.get(3)
    r=client.get('/api/v1.0/users/3',data=json.dumps(user_schema.dump(user)), content_type='application/json')
    data = json.loads(r.get_data(as_text=True))
    assert r.status_code == 200
    assert data['name'] == 'tizia'

def test_post(client):
    n_string = str(n)
    name = 'tzaza'
    j = {
        'name':'tzaza',
        'email': n_string + 'cailzaza@mail.com',
        'description': 'zzzzzzzzzz',
        'avatar': 'https://images.unsplash.com/photo-1558981359-219d6364c9c8?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60'
    }
    r=client.post('/api/v1.0/users', data=json.dumps(j), content_type='application/json')
    assert r.status_code == 200
    global user_id 
    user_id = str(r.json['id'])
    assert r.json['id'] is not None
    assert type(r.json['id']) is int
    assert r.json['email'] is not None
    assert r.json['name'] is not None
    assert type(r.json['name']) is str
    assert r.json['name'] == name

def test_put(client):
    j = {
        'name':'tizia',
        'email':'prova46@mail.com',
        'description': 'prova',
        'avatar': 'https://images.unsplash.com/photo-1558981359-219d6364c9c8?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60'
    }
    r=client.put('/api/v1.0/users/3', data=json.dumps(j), content_type='application/json')
    assert r.status_code == 200

def test_get2(client):
    user = User.query.get(4)
    r=client.get('/api/v1.0/users?user_id=3',data=json.dumps(user_schema.dump(user)), content_type='application/json')
    data = json.loads(r.get_data(as_text=True))
    assert r.status_code == 200
    assert data['name'] == 'tizia'

def test_get_not_found(client):
    r=client.get('/api/v1.0/users/1')
    assert r.status_code == 404

def test_get_not_found_par(client):
    r=client.get('/api/v1.0/users?user_id=1')
    data = json.loads(r.get_data(as_text=True))
    assert data == 'User Not Found'
    


def test_delete(client):
    #user = User.query.filter_by(email= str(n)+'cailzaza@mail.com').first()
    r=client.delete('/api/v1.0/users/'+ user_id)
    assert r.status_code == 200
    r=client.delete('/api/v1.0/users/'+ user_id)
    data = json.loads(r.get_data(as_text=True))
    assert data == 'User Not Found'
    assert r.status_code == 404
    