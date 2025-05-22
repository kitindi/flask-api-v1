from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource,request, abort, fields, marshal_with, reqparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
api = Api(app)



# model

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return f'User(name={self.name}, email={self.email})'

# Validating data 

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required = True, help="Name cannot be blank" )
user_args.add_argument('email', type=str, required = True, help="Email cannot be blank" )


# creating an endpoints for the users resources

userFields = {
    "id":fields.Integer,
    "name": fields.String,
    "email":fields.String
}



class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201
    

# assigning the https events to the api endpoints

api.add_resource(Users, "/api/users/")
@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)