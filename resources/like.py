from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schemas import LikeSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required,get_jwt_identity
from models import Post,Like


blp=Blueprint("likes",__name__)


@blp.route('/post/<post_id>/like')
class LikeList(MethodView):
    @blp.response(200, LikeSchema(many=True))
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post.likes.all()
    
    @blp.arguments(LikeSchema)
    @blp.response(201, LikeSchema)
    @jwt_required()
    def post(self, like_data, post_id):
        user_id = get_jwt_identity()  
        like_value = like_data.get("like") 

       
        if like_value not in [True, False]:
            abort(400, message="The 'like' field must be True (like) or False (dislike).")

        try:
            existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()

            if existing_like:
                existing_like.like = like_value
            else:
                new_like = Like(user_id=user_id, post_id=post_id, like=like_value)
                db.session.add(new_like)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"Database error: {str(e)}")

        return {"message": "Like/Dislike updated successfully", "post_id": post_id, "like": like_value}, 200
