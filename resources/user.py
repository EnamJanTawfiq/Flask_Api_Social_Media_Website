from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token,get_jwt,jwt_required
from blocklist import BLOCKLIST
from db import db
from models import UserModel
from schemas import UserSchema


blp = Blueprint("users", __name__)

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="A user with that email already exists.")
        user = UserModel(
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            role=user_data.get("role", "user") 
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.email == user_data["email"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id), additional_claims={"email": user.email, "role": user.role})
            return {"access_token": access_token}, 200
        abort(401, message="Invalid credentials.")
        


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200
    
    
@blp.route('/users')
class UsersList(MethodView):
    @blp.response(200, UserSchema(many=True) )
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"msg": "Access denied. Admins only"}), 403
        return UserModel.query.all()
    
    
@blp.route('/user/<int:user_id>')
class UsersList(MethodView):
    @blp.response(200, UserSchema)
    @jwt_required()
    def get(self,user_id):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"msg": "Access denied. Admins only"}), 403
        user=UserModel.query.get_or_404(user_id)
        return user
    
    
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    @jwt_required()
    def put(self,user_data,user_id):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"msg": "Access denied. Admins only"}), 403
        user=UserModel.query.get(user_id)
        if user:
            user.email=user_data["email"]
            user.password=user_data["password"]

        else:
            user=UserModel(id=user_id,**user_data)
        db.session.add(user)
        db.session.commit()
        return user
        
    @jwt_required()  
    def delete(self,user_id):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"msg": "Access denied. Admins only"}), 403
        user=UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message":"User Deleted"}
    