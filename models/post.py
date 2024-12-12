from db import db

class Post(db.Model):
    __tablename__ = 'posts'  
    
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(150), nullable=False) 
    description = db.Column(db.Text, nullable=True) 
    image = db.Column(db.String(255), nullable=True)  
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp()) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=False)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    likes = db.relationship('Like', backref='post', lazy='dynamic')

    def __repr__(self):
        return f"<Post {self.title}>"