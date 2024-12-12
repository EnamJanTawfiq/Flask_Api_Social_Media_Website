from flask import request,jsonify
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schemas import PostSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from flask_jwt_extended import jwt_required,get_jwt_identity
from models import Post


blp=Blueprint("posts",__name__)

@blp.route('/post')
class PostList(MethodView):
    @blp.response(200, PostSchema(many=True) )
    def get(self):
        return Post.query.all()
    
    @blp.arguments(PostSchema)
    @blp.response(201, PostSchema)
    @jwt_required()
    def post(self,post_data):
        user_id = get_jwt_identity()
        post=Post(**post_data,user_id=user_id)
        try:
            db.session.add(post)
            db.session.commit()
        except IntegrityError:
            abort(404,"Something missing")
        except SQLAlchemyError:
            abort(404,"Something missed")
        return post




@blp.route('/post/<int:post_id>')
class Posts(MethodView):
    @blp.response(200, PostSchema)
    def get(self,post_id):
        post=Post.query.get_or_404(post_id)
        return post
    
    @blp.arguments(PostSchema)
    @blp.response(200, PostSchema)
    @jwt_required()
    def put(self,post_data,post_id):
        post=Post.query.get(post_id)
        if post:
            post.title=post_data["title"]
            post.description=post_data["description"]
            post.image=post_data["image"]
        else:
            post=Post(id=post_id,**post_data)
        db.session.add(post)
        db.session.commit()
        return post
        
    @jwt_required()  
    def delete(self,post_id):
        post=Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return {"message":"Post Deleted"}
    

