from db import db


class Like(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    like = db.Column(db.Boolean, nullable=False) 
    timestamp = db.Column(db.DateTime, server_default=db.func.now()) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), unique=False, nullable=False)

