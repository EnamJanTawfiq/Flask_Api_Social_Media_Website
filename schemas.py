from marshmallow import Schema, fields, validate

class PostSchema(Schema):
    id = fields.Int(dump_only=True)  
    title = fields.Str(required=True, validate=validate.Length(max=150)) 
    description = fields.Str()  
    image = fields.Str() 
    timestamp = fields.DateTime(dump_only=True)  
    user_id=fields.Int()
    comments = fields.List(fields.Nested(lambda: CommentSchema()), dump_only=True)  
    likes = fields.List(fields.Nested(lambda: LikeSchema()), dump_only=True)  
    
class CommentSchema(Schema):
    id = fields.Int(dump_only=True)  
    content = fields.Str(required=True)  
    user_id=fields.Int()
    post_id = fields.Int()
    
class LikeSchema(Schema):
    id = fields.Int(dump_only=True)
    like=fields.Bool()
    timestamp = fields.DateTime(dump_only=True)
    user_id = fields.Int()
    post_id = fields.Int()

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(required=False)
    timestamp = fields.DateTime(dump_only=True)
    posts = fields.List(fields.Nested(lambda: PostSchema()), dump_only=True)   
    comments = fields.List(fields.Nested(lambda: CommentSchema()), dump_only=True)  
    likes = fields.List(fields.Nested(lambda: LikeSchema()), dump_only=True)  

