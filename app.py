from flask import Flask,jsonify
from flask_migrate import Migrate
from flask_smorest import Api
from db import db
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
app=Flask(__name__)


from resources.user import blp as UserBlueprint
from resources.post import blp as PostBlueprint
from resources.comment import blp as CommentBlueprint
from resources.like import blp as LikeBlueprint




app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Post REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
api = Api(app)
migrate=Migrate(app,db)


app.config["JWT_SECRET_KEY"]='super_secret_key'
jwt=JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )
    
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )



api.register_blueprint(UserBlueprint)
api.register_blueprint(PostBlueprint)
api.register_blueprint(CommentBlueprint)
api.register_blueprint(LikeBlueprint)


