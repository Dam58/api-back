from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__) # app è un istanza della classe Flask
api = Api(app, #the main entry point for the application
        version= '0.1',
        title='The perfect api',
        description='endpoints for class project at ial',
        endpoint='api')



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #variabile d'ambiente
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)

    def asDict(self): #dict è un dizionario che passa i dati del db in (u user?)
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
users = api.namespace('users', description = 'CRUD operation for users') # namespace è un oggetto che racoglie elementi---__-- swagger


usersModel = users.model('usersModel', { #definizione del modello user
    'username' : fields.String(Required=True, validate=True),       # viene visualizzato nello spazio model
    'email' : fields.String(Required=True, validate=True)           # viene visualizzato nello spazio model
})


resp = {200: 'Success', 400: 'user already in db', 406: 'Content not allowed', \
        400: 'Payload to large', 500: 'Server Error'}



#manage status codes
#manage responses

@users.route('')
class Users(Resource):
    #get all users
    #get a user based on id
    def get(self):
        users = User.query.all()
        j = {}
        j ['data'] = []
        j ['metadata'] = {}
        j ['metadata']['n_result'] = User.query.count()#separa la risposta get tra i dati richiesti e il numero di
        j ['metadata']['n_page'] = 1
        for user in users:
            j['data'].append(user.asDict())
        return jsonify(j)

    @users.expect(usersModel, validate=True)
    @users.doc(responses=resp)
    def post(self):
        '''create a new user MODIFIED'''

        try: #gestisce le eccezioni qualunque errore da
            data = request.get_json()
            app.logger.info(data)
            username_request=data.get("username")
            email_request=data.get("email")

        #checking if users exist

        #ifUser.query.filter( (User.username==username_request) | (User.email=email_request).count() > 0):
        #la parte sopra come sotto ma semplificato
            u=User.query.filter_by(username=username_request).first()#query e if per rendere un errore in caso di prima richiesta errata
            if(u is not None):
                return 'User already in DB', 400

            u=User.query.filter_by(email=email_request).first()
            if(u is not None):
                return 'User already in DB', 400

            u = User(username=username_request, email=email_request)
            app.logger.info(type(u))
            db.session.add(u)
            db.session.commit() #devo salvare u(user) nel db
            return jsonify(u.asDict())

        except:
            app.logger.error(traceback.format_exc())
            return 'error server side', 500

        #create a new record in the db
        #return the user and 200

        
    #create a put
@users.route('/<int:user_id>')
class UsersId(Resource):
    def delete(self, user_id):
        '''delete a user'''
        try:
            u = User.query.filter_by(id=user_id).first()
            if(u is None):
                return 'User not found', 404
        db.session.delete(u)
        db.session.commit()
        return  204

        except:
            app.logger.error(traceback.format_exc())
            return 'Error server side', 500



def create_app():
    return app

if __name__ =='__main__':
    app.run(debug=True)

    #write tests
    #show test coverage
