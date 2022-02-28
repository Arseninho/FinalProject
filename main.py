from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
api=Api(app)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config["JWT_SECRET_KEY"] = "my_secret_key"
jwt = JWTManager(app)
db = SQLAlchemy(app)

user_resource_fields={'id':fields.Integer,'username':fields.String, 'email':fields.String, 'password':fields.String}
post_resource_fields={'id':fields.Integer, 'post_id':fields.Integer, 'title':fields.String, 'body':fields.String}


class Auth(Resource):
    def post(self):
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        user=UserModel.query.filter_by(email=email).first()
        if user == None:
            return jsonify({"msg":"User doesn't exist"})
        if email != user.email or check_password_hash(user.password, password):
            return jsonify({"msg":"Wrong username or password"}), 401 


        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token)

class Register(Resource):
    def post(self):
        args=userparser.parse_args()
        user=UserModel(username=args["username"], email=args["email"], password=generate_password_hash(args["password"]))
        db.session.add(user)
        db.session.commit()
        return {"msg":"created"}, 201


class Post(Resource):
    @marshal_with(post_resource_fields)
    def get(self, post_id):
        if post_id==000:
            return PostModel.query.all()
        post=PostModel.query.filter_by(id=post_id).first()
        return post
    def post(self, post_id):
        args=Parser.parse_args()
        user=PostModel(id=args['id'], title=args['title'], body=args['body'], post_id=args['post_id'])
        db.session.add(user)
        db.session.commit()
        return 'post inserted'
    def put(self, id):
        args=Parser.parse_args()
        post=PostModel.query.filter_by(post_id=id).first()
        if post==None:
            post=PostModel(username=args['username'], email=args['email'])
        else:
            user.username=args['username']
            user.email=args['email']
        
        db.session.add(user)
        db.session.commit()
        return 'edited'
    def delete(self, post_id):
        post=PostModel.query.filter_by(id=post_id).first()
        if post==None:
            return f'user with id {post_id} doesnt exist'
        else:    
            db.session.delete(user)
            db.session.commit()        
        return f'user with id {post_id} deleted'



class UserModel(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(20))


    def __repr__(self):
        return '<User %r>' % self.username

class PostModel (db.Model):
    __tablename__="posts"
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(80), nullable=False)
    body=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.title



user=UserModel(username='john', email='john@mail.com')
# db.session.add(user)
# db.session.commit()

Parser=reqparse.RequestParser()
userparser=Parser.add_argument('username', type=str, help='username must be string')
userparser=Parser.add_argument('email', type=str, required=True, help='email must be string')
userparser=Parser.add_argument('password', type=str, required=True, help='password must be string')
postparser=Parser.add_argument('id', type=int, help='id must be string')
postparser=Parser.add_argument('title', type=str, help='title must be string')
postparser=Parser.add_argument('body', type=str, help='body must be string')
postparser=Parser.add_argument('user_id', type=int, help='user_id must be string')


class User(Resource):
    @jwt_required()
    @marshal_with(user_resource_fields)
    def get(self, user_id):
        if user_id==000:
            return UserModel.query.all()
        user=UserModel.query.filter_by(id=user_id).first()
        return user
    @marshal_with(user_resource_fields)
    # @jwt_required()
    def post(self, user_id):
        args=Parser.parse_args()
        password=generate_password_hash(args["password"])
        user=UserModel(username=args['username'], email=args['email'],password=password)
        db.session.add(user)
        db.session.commit()
        return 'user inserted'

    def delete(self, user_id):
        user=UserModel.query.filter_by(id=user_id).first()
        if user==None:
            return f'user with id {user_id} doesnt exist'
        else:    
            db.session.delete(user)
            db.session.commit()        
        return f'user with id {user_id} deleted'

    def put(self, user_id):
        args=Parser.parse_args()
        user=UserModel.query.filter_by(id=user_id).first()
        
        if user==None:
            user=UserModel(username=args['username'], email=args['email'])
        else:
            user.username=args['username']
            user.email=args['email']
        
        db.session.add(user)
        db.session.commit()
        return 'edited'


api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Post, '/post/<int:post_id>')
api.add_resource(Auth, '/login')
api.add_resource(Register, '/register')

if __name__ == '__main__':
    app.run(debug=True)