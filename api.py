from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress warning

db = SQLAlchemy(app)
api = Api(app)



# Model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return f'User(name={self.name}, email={self.email})'

# Validating data 
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

# Response fields
user_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String
}

class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        """Get all users"""
        users = UserModel.query.all()
        return users
    
    @marshal_with(user_fields)
    def post(self):
        """Create a new user"""
        args = user_args.parse_args()
        
        # Check if user with same name or email already exists
        if UserModel.query.filter_by(name=args['name']).first():
            abort(409, message="User with that name already exists")
        if UserModel.query.filter_by(email=args['email']).first():
            abort(409, message="User with that email already exists")
            
        user = UserModel(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201  # Return the created user with 201 status


class User(Resource):
     @marshal_with(user_fields)
     def get(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user :
            abort(404,"User not found")
        return user
         
         
    
        

# Registering resource with API
api.add_resource(Users, "/api/users")
api.add_resource(User, "/api/users/<int:user_id>")

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)