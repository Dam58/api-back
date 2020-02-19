from flask import Flask, jsonify, request, abort
import requests
import json
from flask_restplus import Api, Resource, reqparse, fields
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from flask_cors import CORS, cross_origin

#modified
app = Flask(__name__)

cors = CORS(app)

api = Api(app, version='1.0', title='Sample Users Insert API',
    description='API for insert users in a DB')

users = api.namespace('api/v1.0/users',description='CRUD operation for users')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qjamdtwgrbyppe:02ffd5e72a3b9f6983c048fd6f3d0fdf0457a91f580eb72ce5c807cd40a5fa21@ec2-54-247-125-38.eu-west-1.compute.amazonaws.com:5432/d2qjilevj3ug76' 
app.config['PER_PAGE'] = 6

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    avatar = db.Column(db.String, nullable=True, default='https://shmector.com/_ph/4/184260380.png')
    description = db.Column(db.String, nullable=True)

class UserSchema(ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session

userModel = users.model('userModel', {
    'name' : fields.String(required=True, validate=True),
    'email' : fields.String(required=True, validate=True),
    'description': fields.String(validate=True),
    'avatar' : fields.String(validate=True)
})

user_schema = UserSchema()
users_schema = UserSchema(many=True)

db.create_all()

parserId = reqparse.RequestParser()
parserId.add_argument('user_id',type=int)

parserPage = reqparse.RequestParser()
parserPage.add_argument('page',type=int, default=1)

resp = {200: 'Success', 400: 'User already in db', 406: 'Content not allowed', \
    413: 'Payload too large', 500: 'Server Error', 404: 'User Not Found' }

@users.route('/<int:user_id>')
class GET_User(Resource):
    def get(self,user_id):
        user = User.query.get_or_404(user_id)
        #if not user:
        #   return 'User Not Found', 404
        return jsonify(user_schema.dump(user))
    
    @users.expect(userModel, validate=True)
    def put(self,user_id):
        user = User.query.get_or_404(user_id)
        #if not user:
        #   return 'User Not Found', 404
        print(request.get_json())
        user.name = request.get_json()['name'] if request.get_json()['name'] else user.name
        user.description = request.get_json()['description'] if request.get_json()['description'] else user.description
        user.avatar =  request.get_json()['avatar'] if request.get_json()['avatar'] else user.avatar
        user.email =  request.get_json()['email'] if request.get_json()['email'] else user.email
        db.session.commit()
        return jsonify(user_schema.dump(user))

    def delete(self,user_id):
        try:
            user = User.query.get(user_id)
            if not user:
             return 'User Not Found', 404
            db.session.delete(user)
            db.session.commit()
            return jsonify({'result': True})
        except:
            return 'Error Server Side', 500


@users.route('')
class POST_User(Resource):
    @users.expect(userModel, validate=True)
    @users.doc(responses=resp)
    def post(self):
        try:
            user_name = request.get_json()['name'] 
            user_description = request.get_json()['description']
            user_avatar =  request.get_json()['avatar'] 
            user_email =  request.get_json()['email']
            new_user = User(
            name=user_name,
            email=user_email,
            avatar=user_avatar,
            description=user_description)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(user_schema.dump(new_user))
        except:
            return 'Error Server Side', 500

    @users.expect(parserId, parserPage)
    def get(self):
        if request.args.get('user_id'):
            user_id=request.args.get('user_id')
            user = User.query.get(user_id)
            if not user:
                return 'User Not Found', 404
            return jsonify(user_schema.dump(user))
        else:
            page = request.args.get('page', 1 , type=int)
            users_count = User.query.count()
            pages= users_count // app.config['PER_PAGE'] + (users_count % app.config['PER_PAGE'] > 0)
            users = User.query.paginate(page, app.config['PER_PAGE'], False).items
            response =   { "page": page, "per_page": app.config['PER_PAGE'],
                    "total": users_count, "total_pages": pages, "data": []}
            response["data"]=users_schema.dump(users)
            return jsonify(response)

def create_app():
    return app     


if __name__ == '__main__':
    app.run(debug=True)