from db import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), unique=False, nullable=False)
