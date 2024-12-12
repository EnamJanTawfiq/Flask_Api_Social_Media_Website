from db import db


class UserModel(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp()) 
    posts = db.relationship('Post', backref="user", lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    likes = db.relationship('Like', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f"<User>"