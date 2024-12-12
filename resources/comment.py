from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schemas import CommentSchema,PostSchema
from db import db
from flask_jwt_extended import jwt_required,get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from models import Post,Comment


blp=Blueprint("comments",__name__)

@blp.route('/post/<post_id>/comment')
class CommentList(MethodView):
    @blp.response(200, CommentSchema(many=True))
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post.comments.all()
    
    @blp.arguments(CommentSchema)
    @blp.response(201, CommentSchema)
    @jwt_required()
    def post(self, comment_data, post_id):
        user_id=get_jwt_identity()
        comment = Comment(**comment_data, post_id=post_id,user_id=user_id)
        try:
            db.session.add(comment)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return comment
    
@blp.route('/comment/<comment_id>') 
class Comments(MethodView):
    @blp.response(200, CommentSchema)
    def get(self,comment_id):
        comment=Comment.query.get_or_404(comment_id)
        return comment
    
    @blp.arguments(CommentSchema)
    @blp.response(200, CommentSchema)
    @jwt_required()
    def put(self,comment_data,comment_id):
        comment=Comment.query.get(comment_id)
        if comment:
            comment.content=comment_data["content"]
        else:
            comment=Comment(id=comment_id,**comment_data)
        db.session.add(comment)
        db.session.commit()
        return comment
    @jwt_required()
    def delete(self,comment_id):
        comment=Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        return {"message":"comment Deleted"}
        
    
         

        
            
